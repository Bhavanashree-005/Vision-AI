"""Computer Vision Engine — Core image processing operations and code generation."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
import cv2
import numpy as np
import requests
from src.config import DATA_DIR, logger

# Directory for caching cascade classifiers
CASCADES_DIR = DATA_DIR / "cascades"
CASCADES_DIR.mkdir(parents=True, exist_ok=True)

FACE_CASCADE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
EYE_CASCADE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml"


def download_file(url: str, dest_path: Path) -> bool:
    """Download a file with requests and save to destination path."""
    try:
        logger.info("Downloading XML cascade from %s to %s", url, dest_path)
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        dest_path.write_bytes(response.content)
        return True
    except Exception as exc:
        logger.error("Failed to download cascade XML: %s", exc)
        return False


def get_cascade_path(filename: str, url: str) -> Optional[str]:
    """Retrieve the path to a Haar cascade XML, downloading if missing."""
    # 1. Check local cache
    local_path = CASCADES_DIR / filename
    if local_path.exists() and local_path.stat().st_size > 1000:
        return str(local_path)

    # 2. Check OpenCV package default location
    cv2_dir = Path(cv2.__file__).resolve().parent
    cv2_cascade_path = cv2_dir / "data" / filename
    if cv2_cascade_path.exists():
        return str(cv2_cascade_path)

    # 3. Fallback: Download from GitHub
    success = download_file(url, local_path)
    if success:
        return str(local_path)

    return None


class CVEngine:
    """Handles image processing and dynamic code generation for the CV Lab."""

    @staticmethod
    def apply_basic_filter(
        image_np: np.ndarray, filter_type: str, params: Dict[str, Any]
    ) -> Tuple[np.ndarray, str, Dict[str, Any]]:
        """Apply basic image filters (Grayscale, Blur, Thresholding).

        Returns:
            Tuple of (Processed Image, Python Code Snippet, Metadata).
        """
        # Ensure we have a valid image copy
        img = image_np.copy()
        h, w = img.shape[:2]
        meta = {"dimensions": f"{w}x{h} px"}

        if filter_type == "Grayscale":
            if len(img.shape) == 3:
                processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                processed = img
            code = (
                "import cv2\n\n"
                "# Load the image\n"
                "image = cv2.imread('image.jpg')\n\n"
                "# Convert BGR image to Grayscale\n"
                "gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
                "# Save or display the result\n"
                "cv2.imwrite('result_gray.jpg', gray_image)\n"
            )
            meta["channels"] = 1
            return processed, code, meta

        elif filter_type == "Gaussian Blur":
            ksize = params.get("ksize", 5)
            # kernel size must be odd
            if ksize % 2 == 0:
                ksize += 1
            processed = cv2.GaussianBlur(img, (ksize, ksize), 0)
            code = (
                "import cv2\n\n"
                "# Load the image\n"
                "image = cv2.imread('image.jpg')\n\n"
                "# Apply Gaussian Blur to smooth/reduce noise\n"
                f"blurred = cv2.GaussianBlur(image, ({ksize}, {ksize}), 0)\n\n"
                "# Save or display the result\n"
                "cv2.imwrite('result_blur.jpg', blurred)\n"
            )
            return processed, code, meta

        elif filter_type == "Bilateral Filter":
            d = params.get("d", 9)
            sigma_color = params.get("sigma_color", 75)
            sigma_space = params.get("sigma_space", 75)
            processed = cv2.bilateralFilter(img, d, sigma_color, sigma_space)
            code = (
                "import cv2\n\n"
                "# Load the image\n"
                "image = cv2.imread('image.jpg')\n\n"
                "# Apply Bilateral Filter (reduces noise while keeping edges sharp)\n"
                f"filtered = cv2.bilateralFilter(image, d={d}, sigmaColor={sigma_color}, sigmaSpace={sigma_space})\n\n"
                "# Save or display the result\n"
                "cv2.imwrite('result_bilateral.jpg', filtered)\n"
            )
            return processed, code, meta

        elif filter_type == "Thresholding":
            thresh_val = params.get("thresh_val", 127)
            thresh_type = params.get("thresh_type", "Binary")

            # Must be grayscale for standard thresholding
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            if thresh_type == "Binary":
                _, processed = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
                code_type = "cv2.THRESH_BINARY"
            else:  # Otsu
                thresh_val, processed = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
                code_type = "cv2.THRESH_BINARY + cv2.THRESH_OTSU"

            code = (
                "import cv2\n\n"
                "# Load the image and convert to grayscale\n"
                "image = cv2.imread('image.jpg')\n"
                "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
                "# Apply global thresholding\n"
                f"thresh_val, thresholded = cv2.threshold(gray, {thresh_val}, 255, {code_type})\n\n"
                "# Save or display the result\n"
                "cv2.imwrite('result_threshold.jpg', thresholded)\n"
            )
            meta["actual_threshold"] = thresh_val
            return processed, code, meta

        return img, "# No filter selected\n", meta

    @staticmethod
    def apply_edge_detection(
        image_np: np.ndarray, method: str, params: Dict[str, Any]
    ) -> Tuple[np.ndarray, str, Dict[str, Any]]:
        """Apply edge and line detection algorithms (Canny, Hough)."""
        img = image_np.copy()
        h, w = img.shape[:2]
        meta = {}

        if method == "Canny Edges":
            low = params.get("low_threshold", 50)
            high = params.get("high_threshold", 150)
            processed = cv2.Canny(img, low, high)
            code = (
                "import cv2\n\n"
                "# Load the image\n"
                "image = cv2.imread('image.jpg')\n\n"
                "# Apply Canny edge detection\n"
                f"edges = cv2.Canny(image, threshold1={low}, threshold2={high})\n\n"
                "# Save or display\n"
                "cv2.imwrite('edges.jpg', edges)\n"
            )
            # Count white pixels to give some stats
            edge_pixels = np.sum(processed > 0)
            meta["edge_pixel_percentage"] = f"{(edge_pixels / (h * w)) * 100:.2f}%"
            return processed, code, meta

        elif method == "Hough Lines":
            # 1. Canny edges first
            low = params.get("low_threshold", 50)
            high = params.get("high_threshold", 150)
            edges = cv2.Canny(img, low, high)

            # 2. Hough Lines Probabilistic
            hough_thresh = params.get("hough_threshold", 100)
            min_line_len = params.get("min_line_length", 50)
            max_line_gap = params.get("max_line_gap", 10)

            lines = cv2.HoughLinesP(
                edges, 1, np.pi / 180, hough_thresh, minLineLength=min_line_len, maxLineGap=max_line_gap
            )

            line_count = 0
            if lines is not None:
                line_count = len(lines)
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    # Draw red line
                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

            code = (
                "import cv2\n"
                "import numpy as np\n\n"
                "# Load the image\n"
                "image = cv2.imread('image.jpg')\n\n"
                "# Convert to grayscale and apply Canny edges\n"
                "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
                f"edges = cv2.Canny(gray, threshold1={low}, threshold2={high})\n\n"
                "# Detect lines using Probabilistic Hough Transform\n"
                "lines = cv2.HoughLinesP(\n"
                "    edges,\n"
                "    rho=1,\n"
                "    theta=np.pi/180,\n"
                f"    threshold={hough_thresh},\n"
                f"    minLineLength={min_line_len},\n"
                f"    maxLineGap={max_line_gap}\n"
                ")\n\n"
                "# Draw detected lines on the image\n"
                "if lines is not None:\n"
                "    for line in lines:\n"
                "        x1, y1, x2, y2 = line[0]\n"
                "        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)\n\n"
                "cv2.imwrite('hough_lines.jpg', image)\n"
            )
            meta["lines_detected"] = line_count
            return img, code, meta

        elif method == "Hough Circles":
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            # Smooth to reduce false circles
            gray = cv2.medianBlur(gray, 5)

            dp = params.get("dp", 1)
            min_dist = params.get("min_dist", 50)
            param1 = params.get("param1", 50)
            param2 = params.get("param2", 30)
            min_r = params.get("min_radius", 10)
            max_r = params.get("max_radius", 100)

            circles = cv2.HoughCircles(
                gray,
                cv2.HOUGH_GRADIENT,
                dp=dp,
                minDist=min_dist,
                param1=param1,
                param2=param2,
                minRadius=min_r,
                maxRadius=max_r,
            )

            circle_count = 0
            if circles is not None:
                circles = np.uint16(np.around(circles))
                circle_count = len(circles[0])
                for i in circles[0, :]:
                    # draw the outer circle in green
                    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # draw the center of the circle in red
                    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

            code = (
                "import cv2\n"
                "import numpy as np\n\n"
                "# Load image, convert to grayscale and blur\n"
                "image = cv2.imread('image.jpg')\n"
                "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n"
                "gray = cv2.medianBlur(gray, 5)\n\n"
                "# Apply Hough Circle Transform\n"
                "circles = cv2.HoughCircles(\n"
                "    gray,\n"
                "    cv2.HOUGH_GRADIENT,\n"
                f"    dp={dp},\n"
                f"    minDist={min_dist},\n"
                f"    param1={param1},\n"
                f"    param2={param2},\n"
                f"    minRadius={min_r},\n"
                f"    maxRadius={max_r}\n"
                ")\n\n"
                "# Draw circles on the image\n"
                "if circles is not None:\n"
                "    circles = np.uint16(np.around(circles))\n"
                "    for i in circles[0, :]:\n"
                "        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Outer\n"
                "        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)     # Center\n\n"
                "cv2.imwrite('circles.jpg', image)\n"
            )
            meta["circles_detected"] = circle_count
            return img, code, meta

        return img, "# No edge detection selected\n", meta

    @staticmethod
    def apply_contour_analysis(
        image_np: np.ndarray, params: Dict[str, Any]
    ) -> Tuple[np.ndarray, str, Dict[str, Any]]:
        """Detect and analyze contours."""
        img = image_np.copy()
        h, w = img.shape[:2]

        # Sliders for preprocessing
        low_thresh = params.get("low_threshold", 50)
        high_thresh = params.get("high_threshold", 150)
        min_area = params.get("min_area", 100)

        # 1. Grayscale & Canny
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        edges = cv2.Canny(gray, low_thresh, high_thresh)

        # 2. Find contours
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        contour_details = []
        valid_contours = []

        for idx, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area >= min_area:
                valid_contours.append(cnt)
                perimeter = cv2.arcLength(cnt, True)
                x, y, cw, ch = cv2.boundingRect(cnt)

                # Draw bounding box (blue) and label index
                cv2.rectangle(img, (x, y), (x + cw, y + ch), (255, 0, 0), 2)
                cv2.putText(
                    img,
                    f"#{len(valid_contours)}",
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                )

                contour_details.append(
                    {
                        "id": len(valid_contours),
                        "area": round(area, 1),
                        "perimeter": round(perimeter, 1),
                        "aspect_ratio": round(cw / ch, 2),
                    }
                )

        # Draw actual contour contours in green
        cv2.drawContours(img, valid_contours, -1, (0, 255, 0), 2)

        code = (
            "import cv2\n\n"
            "# Load image and convert to grayscale\n"
            "image = cv2.imread('image.jpg')\n"
            "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
            "# Run Canny to find edges\n"
            f"edges = cv2.Canny(gray, {low_thresh}, {high_thresh})\n\n"
            "# Retrieve contours\n"
            "contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n\n"
            "# Draw and filter contours by area\n"
            "valid_contours = []\n"
            "for cnt in contours:\n"
            f"    if cv2.contourArea(cnt) >= {min_area}:\n"
            "        valid_contours.append(cnt)\n"
            "        # Find bounding boxes\n"
            "        x, y, w, h = cv2.boundingRect(cnt)\n"
            "        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)\n\n"
            "# Draw green outline on original image\n"
            "cv2.drawContours(image, valid_contours, -1, (0, 255, 0), 2)\n\n"
            "cv2.imwrite('contours.jpg', image)\n"
        )

        meta = {
            "total_contours_found": len(contours),
            "contours_after_filter": len(valid_contours),
            "details": contour_details[:10],  # Return up to 10
        }

        return img, code, meta

    @staticmethod
    def detect_faces_and_eyes(image_np: np.ndarray) -> Tuple[np.ndarray, str, Dict[str, Any]]:
        """Local Haar Cascade Face and Eye detection."""
        img = image_np.copy()
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        face_path = get_cascade_path("haarcascade_frontalface_default.xml", FACE_CASCADE_URL)
        eye_path = get_cascade_path("haarcascade_eye.xml", EYE_CASCADE_URL)

        faces_detected = 0
        eyes_detected = 0

        if not face_path:
            meta = {"error": "Could not download face cascade XML file."}
            return img, "# Error loading cascade XML", meta

        face_cascade = cv2.CascadeClassifier(face_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            faces_detected = len(faces)
            eye_cascade = None
            if eye_path:
                eye_cascade = cv2.CascadeClassifier(eye_path)

            for (x, y, w, h) in faces:
                # Draw green face box
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    img, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                )

                # Eye detection within face ROI
                if eye_cascade:
                    roi_gray = gray[y : y + h, x : x + w]
                    roi_color = img[y : y + h, x : x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
                    for (ex, ey, ew, eh) in eyes:
                        # Draw blue eye box
                        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
                        eyes_detected += 1

        code = (
            "import cv2\n\n"
            "# Load image and convert to grayscale\n"
            "image = cv2.imread('image.jpg')\n"
            "gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n"
            "# Load OpenCV pre-trained Haar Cascades\n"
            "face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')\n"
            "eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')\n\n"
            "# Detect faces in the image\n"
            "faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))\n\n"
            "for (x, y, w, h) in faces:\n"
            "    # Draw rectangle around face\n"
            "    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)\n"
            "    \n"
            "    # Region of Interest (ROI) for eyes within the face bounding box\n"
            "    roi_gray = gray[y:y+h, x:x+w]\n"
            "    roi_color = image[y:y+h, x:x+w]\n"
            "    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)\n"
            "    for (ex, ey, ew, eh) in eyes:\n"
            "        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)\n\n"
            "cv2.imwrite('faces_detected.jpg', image)\n"
        )

        meta = {
            "faces_detected": faces_detected,
            "eyes_detected": eyes_detected,
            "cascades_sourced_locally": "Yes",
        }

        return img, code, meta
