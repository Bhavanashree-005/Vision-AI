/* VisionCode AI — Frontend JavaScript Application Module */

document.addEventListener("DOMContentLoaded", () => {
    // --- Application State ---
    let state = {
        currentView: "cv-lab",
        currentCodeTask: "generate",
        cvFile: null,
        visionFile: null,
        chatFile: null,
    };

    // --- DOM Elements ---
    const navItems = document.querySelectorAll(".nav-item");
    const viewSections = document.querySelectorAll(".view-section");
    const statusBanner = document.getElementById("status-banner");
    const apiStatusBadge = document.getElementById("api-status-badge");

    // Check status on load
    checkBackendStatus();

    // ---------------------------------------------------------------------------
    // Navigation Routing
    // ---------------------------------------------------------------------------
    navItems.forEach((item) => {
        item.addEventListener("click", () => {
            const targetView = item.getAttribute("data-view");

            navItems.forEach((n) => n.classList.remove("active"));
            item.classList.add("active");

            if (targetView.startsWith("code-")) {
                const taskType = targetView.replace("code-", "");
                switchCodeTaskView(taskType);
                showSection("view-code-task");
            } else {
                showSection(`view-${targetView}`);
            }
        });
    });

    function showSection(sectionId) {
        viewSections.forEach((sec) => sec.classList.remove("active"));
        const target = document.getElementById(sectionId);
        if (target) {
            target.classList.add("active");
        }
    }

    function switchCodeTaskView(taskType) {
        state.currentCodeTask = taskType;
        const heading = document.getElementById("task-heading");
        const subheading = document.getElementById("task-subheading");
        const label = document.getElementById("task-input-label");
        const textarea = document.getElementById("task-input-text");
        const resultBox = document.getElementById("task-result-box");
        
        resultBox.classList.add("hidden");

        const configs = {
            generate: {
                title: "💻 Generate Python Code",
                subtitle: "Describe the problem, and VisionCode AI will write clean Python code.",
                label: "Describe Problem Statement",
                placeholder: "e.g. Write a Python function using OpenCV to load an image, convert to grayscale, and resize by 50%",
            },
            explain: {
                title: "📖 Explain Python Code",
                subtitle: "Paste Python code to get a line-by-line beginner-friendly breakdown.",
                label: "Paste Python Code",
                placeholder: "# Paste Python or OpenCV code here...",
            },
            debug: {
                title: "🪲 Debug Traceback / Error",
                subtitle: "Paste an error message or buggy code to identify and fix root causes.",
                label: "Paste Error Traceback / Buggy Code",
                placeholder: "e.g. cv2.error: OpenCV(4.8.0) ... assertion failed (!empty())",
            },
            improve: {
                title: "⚡ Improve & Optimize Code",
                subtitle: "Refactor code for performance, readability, and PEP 8 standards.",
                label: "Paste Python Code",
                placeholder: "def process(img):\n    # Paste unoptimized code",
            },
            comment: {
                title: "📝 Add Code Comments",
                subtitle: "Automatically insert helpful explanations throughout source code.",
                label: "Paste Python Code",
                placeholder: "# Paste uncommented Python code here",
            },
        };

        const cfg = configs[taskType] || configs.generate;
        heading.textContent = cfg.title;
        subheading.textContent = cfg.subtitle;
        label.textContent = cfg.label;
        textarea.placeholder = cfg.placeholder;
        textarea.value = "";
    }

    // ---------------------------------------------------------------------------
    // API & Status Helpers
    // ---------------------------------------------------------------------------
    async function checkBackendStatus() {
        try {
            const res = await fetch("/api/status");
            const data = await res.json();
            if (data.api_key_configured) {
                apiStatusBadge.textContent = "✅ Configured";
                apiStatusBadge.className = "badge badge-success";
                statusBanner.classList.add("hidden");
            } else {
                apiStatusBadge.textContent = "⚠️ Not Set";
                apiStatusBadge.className = "badge badge-warning";
                statusBanner.classList.remove("hidden");
            }
        } catch (err) {
            console.error("Status check failed:", err);
        }
    }

    // Save API key
    document.getElementById("save-api-key-btn").addEventListener("click", async () => {
        const input = document.getElementById("api-key-input");
        const key = input.value.trim();
        if (!key) return;

        const formData = new FormData();
        formData.append("api_key", key);

        try {
            const res = await fetch("/api/config/api_key", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                alert("API Key saved successfully!");
                input.value = "";
                checkBackendStatus();
            }
        } catch (err) {
            alert("Failed to save API key: " + err);
        }
    });

    // ---------------------------------------------------------------------------
    // CV Lab (Playground) Logic
    // ---------------------------------------------------------------------------
    const cvFileInput = document.getElementById("cv-file-input");
    const cvFileName = document.getElementById("cv-file-name");
    const origImgPreview = document.getElementById("orig-img-preview");
    const origPlaceholder = document.getElementById("orig-placeholder");

    cvFileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            state.cvFile = file;
            cvFileName.textContent = file.name;

            const reader = new FileReader();
            reader.onload = (event) => {
                origImgPreview.src = event.target.result;
                origImgPreview.classList.remove("hidden");
                origPlaceholder.classList.add("hidden");
            };
            reader.readAsDataURL(file);
        }
    });

    // CV Dynamic Sliders Mapping
    const cvCategorySelect = document.getElementById("cv-category-select");
    const cvOperationSelect = document.getElementById("cv-operation-select");
    const cvSlidersContainer = document.getElementById("cv-dynamic-sliders");

    const cvOperationsMap = {
        "Basic Filters": ["Grayscale", "Gaussian Blur", "Bilateral Filter", "Thresholding"],
        "Edge & Line Detection": ["Canny Edges", "Hough Lines", "Hough Circles"],
        "Contour Analytics": ["Contour Analytics"],
        "Face & Eye Tracking": ["Face & Eye Tracking"],
    };

    function updateCvOperations() {
        const category = cvCategorySelect.value;
        const ops = cvOperationsMap[category] || [];
        cvOperationSelect.innerHTML = "";
        ops.forEach((op) => {
            const opt = document.createElement("option");
            opt.value = op;
            opt.textContent = op;
            cvOperationSelect.appendChild(opt);
        });
        updateCvSliders();
    }

    function updateCvSliders() {
        const op = cvOperationSelect.value;
        cvSlidersContainer.innerHTML = "";

        if (op === "Gaussian Blur") {
            createSlider("ksize", "Kernel Size (Blur Intensity)", 1, 31, 5, 2);
        } else if (op === "Bilateral Filter") {
            createSlider("d", "Diameter (d)", 1, 15, 9, 1);
            createSlider("sigma_color", "Sigma Color", 10, 150, 75, 5);
            createSlider("sigma_space", "Sigma Space", 10, 150, 75, 5);
        } else if (op === "Thresholding") {
            createRadio("thresh_type", "Threshold Type", ["Binary", "Otsu"]);
            createSlider("thresh_val", "Threshold Value", 0, 255, 127, 1);
        } else if (op === "Canny Edges" || op === "Hough Lines") {
            createSlider("low_threshold", "Canny Low Threshold", 0, 255, 50, 5);
            createSlider("high_threshold", "Canny High Threshold", 0, 255, 150, 5);

            if (op === "Hough Lines") {
                createSlider("hough_threshold", "Hough Threshold", 10, 300, 100, 5);
                createSlider("min_line_length", "Min Line Length", 10, 200, 50, 5);
                createSlider("max_line_gap", "Max Line Gap", 1, 50, 10, 1);
            }
        } else if (op === "Hough Circles") {
            createSlider("dp", "Resolution DP", 1, 5, 1, 1);
            createSlider("min_dist", "Min Center Distance", 10, 200, 50, 5);
            createSlider("param1", "Edge Threshold (Param1)", 10, 200, 50, 5);
            createSlider("param2", "Accumulator Threshold (Param2)", 10, 100, 30, 2);
            createSlider("min_radius", "Min Radius", 0, 100, 10, 2);
            createSlider("max_radius", "Max Radius", 10, 500, 100, 10);
        } else if (op === "Contour Analytics") {
            createSlider("low_threshold", "Canny Low Threshold", 1, 255, 50, 5);
            createSlider("high_threshold", "Canny High Threshold", 1, 255, 150, 5);
            createSlider("min_area", "Min Contour Area", 10, 5000, 100, 50);
        }
    }

    function createSlider(id, label, min, max, val, step) {
        const div = document.createElement("div");
        div.className = "slider-group";
        div.innerHTML = `
            <div class="slider-header">
                <span>${label}</span>
                <span id="val-${id}">${val}</span>
            </div>
            <input type="range" id="param-${id}" min="${min}" max="${max}" value="${val}" step="${step}" data-param="${id}" />
        `;
        cvSlidersContainer.appendChild(div);

        const slider = div.querySelector("input");
        const valSpan = div.querySelector(`#val-${id}`);
        slider.addEventListener("input", (e) => {
            valSpan.textContent = e.target.value;
        });
    }

    function createRadio(id, label, options) {
        const div = document.createElement("div");
        div.className = "form-group";
        div.innerHTML = `
            <label>${label}</label>
            <select id="param-${id}" data-param="${id}">
                ${options.map((o) => `<option value="${o}">${o}</option>`).join("")}
            </select>
        `;
        cvSlidersContainer.appendChild(div);
    }

    cvCategorySelect.addEventListener("change", updateCvOperations);
    cvOperationSelect.addEventListener("change", updateCvSliders);
    updateCvOperations();

    // Run CV Process
    document.getElementById("run-cv-btn").addEventListener("click", async () => {
        if (!state.cvFile) {
            alert("Please upload an image first.");
            return;
        }

        const category = cvCategorySelect.value;
        const operation = cvOperationSelect.value;

        // Collect params from dynamic sliders
        const params = {};
        const paramInputs = cvSlidersContainer.querySelectorAll("[data-param]");
        paramInputs.forEach((input) => {
            const key = input.getAttribute("data-param");
            const val = input.type === "range" ? Number(input.value) : input.value;
            params[key] = val;
        });

        const formData = new FormData();
        formData.append("file", state.cvFile);
        formData.append("task_category", category);
        formData.append("operation", operation);
        formData.append("params_json", JSON.stringify(params));

        const btn = document.getElementById("run-cv-btn");
        btn.textContent = "⏳ Processing...";
        btn.disabled = true;

        try {
            const res = await fetch("/api/cv/process", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                // Set processed image
                const procImg = document.getElementById("proc-img-preview");
                const procPlaceholder = document.getElementById("proc-placeholder");
                procImg.src = data.image_b64;
                procImg.classList.remove("hidden");
                procPlaceholder.classList.add("hidden");

                // Set code
                document.getElementById("cv-code-display").textContent = data.code;

                // Render metadata
                const metaContainer = document.getElementById("cv-metadata-container");
                metaContainer.innerHTML = "";
                if (data.metadata) {
                    for (const [k, v] of Object.entries(data.metadata)) {
                        if (k === "details") continue;
                        const card = document.createElement("div");
                        card.className = "meta-card";
                        card.innerHTML = `
                            <div class="meta-label">${k.replace(/_/g, " ")}</div>
                            <div class="meta-value">${v}</div>
                        `;
                        metaContainer.appendChild(card);
                    }
                }
            } else {
                alert("CV Processing error: " + data.detail);
            }
        } catch (err) {
            alert("Error processing image: " + err);
        } finally {
            btn.textContent = "🚀 Process Image";
            btn.disabled = false;
        }
    });

    // Copy CV Code
    document.getElementById("copy-cv-code-btn").addEventListener("click", () => {
        const code = document.getElementById("cv-code-display").textContent;
        navigator.clipboard.writeText(code);
        alert("Python OpenCV code copied to clipboard!");
    });

    // ---------------------------------------------------------------------------
    // AI Vision Assistant
    // ---------------------------------------------------------------------------
    const visionFileInput = document.getElementById("vision-file-input");
    const visionFileName = document.getElementById("vision-file-name");

    visionFileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            state.visionFile = file;
            visionFileName.textContent = file.name;
        }
    });

    document.getElementById("run-vision-btn").addEventListener("click", async () => {
        const query = document.getElementById("vision-query-input").value.trim();
        if (!state.visionFile) {
            alert("Please upload an image screenshot first.");
            return;
        }
        if (!query) {
            alert("Please enter a question or instruction.");
            return;
        }

        const formData = new FormData();
        formData.append("file", state.visionFile);
        formData.append("query", query);

        const btn = document.getElementById("run-vision-btn");
        btn.textContent = "⏳ Examining Screenshot...";
        btn.disabled = true;

        try {
            const res = await fetch("/api/ai/vision", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                const box = document.getElementById("vision-result-box");
                const content = document.getElementById("vision-result-content");
                content.innerHTML = marked.parse(data.result);
                box.classList.remove("hidden");
            }
        } catch (err) {
            alert("Vision analysis failed: " + err);
        } finally {
            btn.textContent = "🚀 Analyze Screenshot";
            btn.disabled = false;
        }
    });

    // ---------------------------------------------------------------------------
    // Code Tasks Handler (Generate, Explain, Debug, Improve, Comment)
    // ---------------------------------------------------------------------------
    document.getElementById("run-task-btn").addEventListener("click", async () => {
        const input = document.getElementById("task-input-text").value.trim();
        if (!input) {
            alert("Please enter your input or code first.");
            return;
        }

        const formData = new FormData();
        formData.append("task", state.currentCodeTask);
        formData.append("user_input", input);

        const btn = document.getElementById("run-task-btn");
        btn.textContent = "⏳ VisionCode AI Thinking...";
        btn.disabled = true;

        try {
            const res = await fetch("/api/ai/task", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                const box = document.getElementById("task-result-box");
                const content = document.getElementById("task-result-content");
                content.innerHTML = marked.parse(data.result);
                box.classList.remove("hidden");
            }
        } catch (err) {
            alert("Task failed: " + err);
        } finally {
            btn.textContent = "🚀 Run Task";
            btn.disabled = false;
        }
    });

    // ---------------------------------------------------------------------------
    // AI Chat
    // ---------------------------------------------------------------------------
    const chatContainer = document.getElementById("chat-messages-container");
    const chatInput = document.getElementById("chat-text-input");
    const chatSendBtn = document.getElementById("chat-send-btn");
    const chatAttachBtn = document.getElementById("chat-attach-btn");
    const chatFileInput = document.getElementById("chat-file-input");
    const chatFileIndicator = document.getElementById("chat-file-indicator");
    const chatFileName = document.getElementById("chat-file-name");

    chatAttachBtn.addEventListener("click", () => chatFileInput.click());
    chatFileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            state.chatFile = file;
            chatFileName.textContent = file.name;
            chatFileIndicator.classList.remove("hidden");
        }
    });

    async function sendChatMessage() {
        const msg = chatInput.value.trim();
        if (!msg && !state.chatFile) return;

        // Render user message
        const userBubble = document.createElement("div");
        userBubble.className = "chat-bubble user";
        userBubble.textContent = msg + (state.chatFile ? ` [Attached: ${state.chatFile.name}]` : "");
        chatContainer.appendChild(userBubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        chatInput.value = "";

        const formData = new FormData();
        let endpoint = "/api/ai/task";

        if (state.chatFile) {
            endpoint = "/api/ai/vision";
            formData.append("file", state.chatFile);
            formData.append("query", msg);
        } else {
            formData.append("task", "chat");
            formData.append("user_input", msg);
        }

        try {
            const res = await fetch(endpoint, { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                const botBubble = document.createElement("div");
                botBubble.className = "chat-bubble assistant";
                botBubble.innerHTML = marked.parse(data.result);
                chatContainer.appendChild(botBubble);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        } catch (err) {
            console.error("Chat error:", err);
        } finally {
            state.chatFile = null;
            chatFileIndicator.classList.add("hidden");
        }
    }

    chatSendBtn.addEventListener("click", sendChatMessage);
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendChatMessage();
    });

    // Clear history
    document.getElementById("clear-history-btn").addEventListener("click", async () => {
        try {
            await fetch("/api/ai/clear_history", { method: "POST" });
            chatContainer.innerHTML = '<div class="chat-bubble assistant">👋 Chat memory cleared. How can I help you?</div>';
            alert("Chat history cleared!");
        } catch (err) {
            console.error("Failed to clear history:", err);
        }
    });

    // Global copy buttons
    document.querySelectorAll(".copy-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-target");
            const el = document.getElementById(targetId);
            if (el) {
                navigator.clipboard.writeText(el.innerText);
                alert("Result copied to clipboard!");
            }
        });
    });
});
