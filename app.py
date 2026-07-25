"""VisionCode AI — Professional Streamlit Frontend.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import io
import sys
import base64
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
import streamlit as st

# -- Ensure src/ is importable --
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.ai_service import AIService
from src.config import get_api_key, logger
from src.utils import read_file_content, save_response_to_file
from src.cv_engine import CVEngine

# ---------------------------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="VisionCode AI — Intelligent CV & Code Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom premium styling using injected CSS
st.markdown(
    """<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}
.title-gradient {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.8rem !important;
    margin-bottom: 0.1rem !important;
}
.subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 1.5rem !important;
}
section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}
.cv-stat-card {
    background: rgba(30, 41, 59, 0.45);
    padding: 1.25rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}
.cv-stat-label {
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.cv-stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #38bdf8;
}
div.stButton > button:first-child {
    background: linear-gradient(135deg, #38bdf8 0%, #0369a1 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.25rem;
    font-weight: 600;
    transition: all 0.25s ease;
    box-shadow: 0 4px 10px rgba(56, 189, 248, 0.15);
}
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    box-shadow: 0 6px 15px rgba(56, 189, 248, 0.25);
    transform: translateY(-1px);
    border: none;
}
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(56, 189, 248, 0), rgba(56, 189, 248, 0.3), rgba(56, 189, 248, 0));
    margin: 1.5rem 0;
}
</style>""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session State Initialisation
# ---------------------------------------------------------------------------

if "service" not in st.session_state:
    st.session_state.service = AIService()

if "response" not in st.session_state:
    st.session_state.response = ""

if "api_key_configured" not in st.session_state:
    st.session_state.api_key_configured = get_api_key() is not None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ---------------------------------------------------------------------------
# Sidebar Area
# ---------------------------------------------------------------------------

with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        width=70,
    )
    st.markdown("## **VisionCode AI**")
    st.caption("Intelligent Computer Vision & Python Assistant")

    st.divider()

    # Navigation choices
    nav = st.radio(
        "Navigation",
        [
            "CV Lab (Playground)",
            "AI Vision Assistant",
            "Generate Code",
            "Explain Code",
            "Debug Error",
            "Improve Code",
            "Add Comments",
            "AI Chat (Code & Vision)",
        ],
    )

    st.divider()

    # API Configuration Panel
    with st.expander("API & AI Model Settings", expanded=not st.session_state.api_key_configured):
        api_status = (
            "✅ Configured" if st.session_state.api_key_configured else "⚠️ Not Set"
        )
        st.caption(f"Status: {api_status}")

        key_input = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="sk-or-...",
            label_visibility="collapsed",
            help="Enter your OpenRouter API key. Get one at openrouter.ai/keys",
        )
        if key_input:
            st.session_state.service.update_api_key(key_input)
            st.session_state.api_key_configured = True
            st.success("API key configured!")
            st.rerun()

        if not st.session_state.api_key_configured:
            st.info(
                "No API key detected. The app runs offline for standard code template assistance "
                "but supports full **local OpenCV** operations in the CV Lab!"
            )

    # Clear & Export operations
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.service.reset_history()
        st.session_state.chat_messages = []
        st.session_state.response = ""
        st.success("Chat history cleared!")
        st.rerun()

    if st.button("💾 Export Chat History", use_container_width=True):
        text = st.session_state.service.get_exports()
        if text.strip():
            st.download_button(
                label="📥 Download .txt",
                data=text,
                file_name="visioncode_chat_history.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.info("No chat history to export.")

    st.divider()
    st.caption("Internship Minor Project · Streamlit · OpenCV")

# ---------------------------------------------------------------------------
# Main Title Header
# ---------------------------------------------------------------------------

st.markdown('<div class="title-gradient">VisionCode AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">An advanced Computer Vision playground and multi-modal Python AI coding assistant</div>',
    unsafe_allow_html=True,
)

if not st.session_state.api_key_configured:
    st.warning(
        "Offline Mode Active: Local Computer Vision functions run offline. To analyze screenshots "
        "or get fully customized code recommendations, enter an OpenRouter API key in the sidebar.",
        icon="⚠️",
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Helper: run AI calls
# ---------------------------------------------------------------------------

def run_ai(method, arg_key: str = "user_input") -> None:
    """Execute AI helper method, capturing responses."""
    user_input = st.session_state.get(arg_key, "")
    if not user_input.strip():
        st.error("Please enter your input or code first.")
        return

    try:
        with st.spinner("Analyzing with VisionCode AI..."):
            response = method(user_input)
        st.session_state.response = response
    except Exception as exc:
        logger.exception("AI Call Failed")
        st.error(f"Something went wrong: {exc}")
        st.session_state.response = ""


def display_output_panel() -> None:
    """Render output panel with copy/download options."""
    response = st.session_state.response
    if not response:
        st.info("Results will appear here.")
        return

    st.markdown("### 📄 Result Output")
    st.markdown(response)

    col1, col2 = st.columns([1, 5])
    with col1:
        st.button(
            "📋 Copy to Clipboard",
            key="copy_btn",
            on_click=_copy_to_clipboard,
            args=(response,),
        )
    with col2:
        saved = save_response_to_file(response, "response")
        if saved:
            st.success(f"Saved response to `{saved.name}`", icon="💾")


def _copy_to_clipboard(text: str) -> None:
    st.write(
        f'<textarea id="hidden_copy" style="position:fixed;left:-9999px">{text}</textarea>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<script>"
        "let ta = document.getElementById('hidden_copy');"
        "ta.select(); document.execCommand('copy');"
        "</script>",
        unsafe_allow_html=True,
    )
    st.toast("Copied to clipboard!", icon="✅")


def file_upload_ui() -> str:
    uploaded = st.file_uploader(
        "Upload a python file",
        type=["py", "txt"],
        label_visibility="collapsed",
        key="file_uploader_code",
    )
    if uploaded is not None:
        try:
            content = uploaded.read().decode("utf-8")
            st.success(f"Loaded `{uploaded.name}`")
            return content
        except Exception as exc:
            st.error(f"Failed to read file: {exc}")
    return ""

# ---------------------------------------------------------------------------
# Page: CV Lab (Playground)
# ---------------------------------------------------------------------------

if nav == "CV Lab (Playground)":
    st.header("🔬 Interactive Computer Vision Playground")
    st.markdown(
        "Upload an image and apply real-time Computer Vision filters. "
        "The corresponding, executable Python OpenCV code will be generated automatically!"
    )

    uploaded_img = st.file_uploader("Select an Image", type=["jpg", "jpeg", "png"])

    if uploaded_img:
        # Load and verify image
        try:
            image = Image.open(uploaded_img).convert("RGB")
            img_np = np.array(image)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        except Exception as exc:
            st.error(f"Error loading image: {exc}")
            st.stop()

        # Side bar columns
        cv_col1, cv_col2 = st.columns([1, 2])

        with cv_col1:
            st.subheader("⚙️ OpenCV Parameters")
            cv_task = st.selectbox(
                "CV Operation Category",
                [
                    "Basic Filters",
                    "Edge & Line Detection",
                    "Contour Analytics",
                    "Face & Eye Tracking",
                ],
            )

            processed_img = None
            generated_code = ""
            metadata = {}

            if cv_task == "Basic Filters":
                filter_type = st.selectbox(
                    "Select Filter",
                    ["Grayscale", "Gaussian Blur", "Bilateral Filter", "Thresholding"],
                )
                params = {}
                if filter_type == "Gaussian Blur":
                    params["ksize"] = st.slider("Kernel Size (Blur Intensity)", 1, 31, 5, step=2)
                elif filter_type == "Bilateral Filter":
                    params["d"] = st.slider("Diameter (d)", 1, 15, 9)
                    params["sigma_color"] = st.slider("Sigma Color", 10, 150, 75)
                    params["sigma_space"] = st.slider("Sigma Space", 10, 150, 75)
                elif filter_type == "Thresholding":
                    params["thresh_type"] = st.radio("Threshold Type", ["Binary", "Otsu"])
                    if params["thresh_type"] == "Binary":
                        params["thresh_val"] = st.slider("Threshold Value", 0, 255, 127)

                processed_img, generated_code, metadata = CVEngine.apply_basic_filter(
                    img_bgr, filter_type, params
                )

            elif cv_task == "Edge & Line Detection":
                edge_method = st.selectbox(
                    "Method", ["Canny Edges", "Hough Lines", "Hough Circles"]
                )
                params = {}
                if edge_method in ["Canny Edges", "Hough Lines"]:
                    params["low_threshold"] = st.slider("Canny Low Threshold", 0, 255, 50)
                    params["high_threshold"] = st.slider("Canny High Threshold", 0, 255, 150)

                if edge_method == "Hough Lines":
                    params["hough_threshold"] = st.slider("Hough Threshold", 10, 300, 100)
                    params["min_line_length"] = st.slider("Min Line Length", 10, 200, 50)
                    params["max_line_gap"] = st.slider("Max Line Gap", 1, 50, 10)

                elif edge_method == "Hough Circles":
                    params["dp"] = st.slider("Resolution DP", 1, 5, 1)
                    params["min_dist"] = st.slider("Min Distance between Centers", 10, 200, 50)
                    params["param1"] = st.slider("Edge Threshold (Param1)", 10, 200, 50)
                    params["param2"] = st.slider("Accumulator Threshold (Param2)", 10, 100, 30)
                    params["min_radius"] = st.slider("Min Radius", 0, 100, 10)
                    params["max_radius"] = st.slider("Max Radius", 10, 500, 100)

                processed_img, generated_code, metadata = CVEngine.apply_edge_detection(
                    img_bgr, edge_method, params
                )

            elif cv_task == "Contour Analytics":
                params = {
                    "low_threshold": st.slider("Canny Low Threshold", 1, 255, 50),
                    "high_threshold": st.slider("Canny High Threshold", 1, 255, 150),
                    "min_area": st.slider("Min Contour Area", 10, 5000, 100),
                }
                processed_img, generated_code, metadata = CVEngine.apply_contour_analysis(
                    img_bgr, params
                )

            elif cv_task == "Face & Eye Tracking":
                st.info("Detects faces (green) and eyes (blue) locally using offline Haar Cascades.")
                with st.spinner("Detecting features..."):
                    processed_img, generated_code, metadata = CVEngine.detect_faces_and_eyes(img_bgr)

            # Metadata Display Cards
            st.subheader("📊 Operation Metadata")
            if metadata:
                for k, v in metadata.items():
                    if k == "details":  # skip nested list
                        continue
                    st.markdown(
                        f"""
                        <div class="cv-stat-card">
                            <div class="cv-stat-label">{k.replace('_', ' ')}</div>
                            <div class="cv-stat-value">{v}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                # If we have contour details, display as table
                if "details" in metadata and metadata["details"]:
                    st.markdown("**Contour Details (Top 5)**")
                    st.table(metadata["details"][:5])

        with cv_col2:
            st.subheader("🖼️ Visual Output")
            tab_orig, tab_proc = st.tabs(["Original Image", "Processed Image"])
            with tab_orig:
                st.image(image, caption="Original uploaded image", use_container_width=True)
            with tab_proc:
                if processed_img is not None:
                    # Convert processed BGR back to RGB or Grayscale for display
                    if len(processed_img.shape) == 2:
                        st.image(processed_img, caption="Processed Output (Grayscale)", use_container_width=True)
                    else:
                        rgb_out = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
                        st.image(rgb_out, caption="Processed Output (Color / Overlays)", use_container_width=True)
                else:
                    st.info("Apply an operation to see the processed output.")

            # Code display
            st.markdown("### 💻 Executable Python OpenCV Code")
            st.code(generated_code, language="python")
            st.download_button(
                label="📥 Download Python Code",
                data=generated_code,
                file_name=f"cv_{cv_task.lower().replace(' ', '_')}.py",
                mime="text/plain",
            )
    else:
        st.info("Please upload an image to begin the Computer Vision interactive playground.")

# ---------------------------------------------------------------------------
# Page: AI Vision Assistant
# ---------------------------------------------------------------------------

elif nav == "AI Vision Assistant":
    st.header("👁️ AI Vision Assistant")
    st.markdown(
        "Upload a screenshot of **code**, **traceback errors**, **system diagrams**, "
        "or **UI mockups** and ask VisionCode AI to analyze, explain, or write code for it."
    )

    uploaded_screen = st.file_uploader(
        "Upload Image / Screenshot", type=["png", "jpg", "jpeg"], key="vision_uploader"
    )
    user_query = st.text_area(
        "What should VisionCode AI do with this image?",
        height=100,
        placeholder="e.g. Explain this error screenshot and show how to fix it, or write Streamlit code to match this UI layout.",
        key="vision_query",
    )

    if st.button("🚀 Analyze Screenshot", type="primary"):
        if not uploaded_screen:
            st.error("Please upload an image/screenshot first.")
        elif not user_query.strip():
            st.error("Please enter a question or query.")
        else:
            img_bytes = uploaded_screen.read()
            mime_type = uploaded_screen.type

            try:
                with st.spinner("AI is examining the image and drafting solution..."):
                    response = st.session_state.service.vision_analyze(
                        user_query, img_bytes, mime_type
                    )
                st.session_state.response = response
            except Exception as exc:
                st.error(f"Vision analysis failed: {exc}")
                st.session_state.response = ""

            st.rerun()

    display_output_panel()

# ---------------------------------------------------------------------------
# Page: Generate Code
# ---------------------------------------------------------------------------

elif nav == "Generate Code":
    st.header("💻 Generate Python Code")
    st.markdown("Describe the programming problem, and VisionCode AI will write clean, well-commented Python code.")

    st.text_area(
        "Describe the problem / requirement:",
        height=180,
        key="user_input",
        placeholder="e.g. Write a Python function using OpenCV to load an image, convert it to grayscale, and resize it by 50%",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        st.button(
            "🚀 Generate",
            type="primary",
            on_click=run_ai,
            args=(st.session_state.service.generate_code,),
        )

    display_output_panel()

# ---------------------------------------------------------------------------
# Page: Explain Code
# ---------------------------------------------------------------------------

elif nav == "Explain Code":
    st.header("📖 Explain Python Code")
    st.markdown("Paste code or load a file to get a line-by-line breakdown of how it works.")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.text_area(
            "Paste Python / CV code:",
            height=250,
            key="user_input",
            placeholder="# Paste your code here to get an explanation",
        )

    with col_right:
        file_code = file_upload_ui()
        if file_code and not st.session_state.get("user_input", ""):
            st.session_state.user_input = file_code
            st.rerun()

    st.button(
        "🚀 Explain",
        type="primary",
        on_click=run_ai,
        args=(st.session_state.service.explain_code,),
    )

    display_output_panel()

# ---------------------------------------------------------------------------
# Page: Debug Error
# ---------------------------------------------------------------------------

elif nav == "Debug Error":
    st.header("🪲 Debug Traceback / Error")
    st.markdown("Paste error logs, tracebacks, or buggy code to identify and fix the issue.")

    st.text_area(
        "Paste the traceback/code details:",
        height=200,
        key="user_input",
        placeholder="e.g. cv2.error: OpenCV(4.8.0) ... assertion failed (!empty()) in cv::CascadeClassifier::detectMultiScale",
    )

    st.button(
        "🚀 Debug",
        type="primary",
        on_click=run_ai,
        args=(st.session_state.service.debug_error,),
    )

    display_output_panel()

# ---------------------------------------------------------------------------
# Page: Improve Code
# ---------------------------------------------------------------------------

elif nav == "Improve Code":
    st.header("⚡ Improve & Optimize Code")
    st.markdown("Paste code to refactor, speed up, or clean up according to PEP 8 standards.")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.text_area(
            "Paste Python / CV code:",
            height=250,
            key="user_input",
            placeholder="def preprocess(img):\n    # paste inefficient code",
        )

    with col_right:
        file_code = file_upload_ui()
        if file_code and not st.session_state.get("user_input", ""):
            st.session_state.user_input = file_code
            st.rerun()

    st.button(
        "🚀 Optimize",
        type="primary",
        on_click=run_ai,
        args=(st.session_state.service.improve_code,),
    )

    display_output_panel()

# ---------------------------------------------------------------------------
# Page: Add Comments
# ---------------------------------------------------------------------------

elif nav == "Add Comments":
    st.header("📝 Add Code Comments")
    st.markdown("Add detailed documentation and explanations directly into your source code.")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.text_area(
            "Paste Python / CV code:",
            height=250,
            key="user_input",
            placeholder="# Paste uncommented Python code here",
        )

    with col_right:
        file_code = file_upload_ui()
        if file_code and not st.session_state.get("user_input", ""):
            st.session_state.user_input = file_code
            st.rerun()

    st.button(
        "🚀 Add Comments",
        type="primary",
        on_click=run_ai,
        args=(st.session_state.service.add_comments,),
    )

    display_output_panel()

# ---------------------------------------------------------------------------
# Page: AI Chat (Code & Vision)
# ---------------------------------------------------------------------------

elif nav == "AI Chat (Code & Vision)":
    st.header("💬 AI Chat (Code & Vision)")
    st.markdown("Ask anything about Python coding, Computer Vision algorithms, math, or logic.")

    # Show chat messages
    for msg in st.session_state.chat_messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f"**🧑 You:** {content}")
        else:
            with st.chat_message("assistant"):
                st.markdown(content)

    # Optional image attachment in Chat
    st.markdown("---")
    chat_file = st.file_uploader(
        "📎 Optional: Attach image to next message", type=["png", "jpg", "jpeg"], key="chat_file_uploader"
    )

    # Message input form
    chat_query = st.chat_input("Ask a question about programming or CV...")

    if chat_query:
        # Append User Message
        st.session_state.chat_messages.append({"role": "user", "content": chat_query})
        
        try:
            with st.spinner("AI is typing..."):
                if chat_file:
                    # Vision analysis chat
                    img_bytes = chat_file.read()
                    mime_type = chat_file.type
                    reply = st.session_state.service.vision_analyze(chat_query, img_bytes, mime_type)
                else:
                    # Standard chat
                    reply = st.session_state.service.chat(chat_query)

                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        except Exception as exc:
            logger.exception("Chat Failed")
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": f"Failed to get response: {exc}"}
            )
        
        st.rerun()

    if st.session_state.chat_messages:
        st.divider()
        export_text = st.session_state.service.get_exports()
        st.download_button(
            "📥 Export Chat Transcript",
            data=export_text,
            file_name="visioncode_chat_transcript.txt",
            mime="text/plain",
        )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.caption(
    "VisionCode AI · Advanced Computer Vision Lab & AI Assistant · "
    "Powered by OpenCV & OpenRouter · v2.0.0"
)