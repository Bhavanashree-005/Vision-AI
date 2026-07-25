<div align="center">

#  AI Code Assistant

**A smart Python coding companion — generate, explain, debug, improve, and comment on Python code using AI.**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
|  **Generate Code** | Describe a problem and get clean Python code |
|  **Explain Code** | Paste code and get a beginner-friendly explanation |
|  **Debug Error** | Paste an error and get the root cause + fix |
|  **Improve Code** | Refactor code for readability and performance |
|  **Add Comments** | Automatically add meaningful comments |
|  **AI Chat** | Ask general Python questions conversationally |

**Plus:**
-  **Offline mode** — works without internet / API key
-  **File upload** — read code directly from `.py` files
-  **Copy & download** — clipboard copy + .txt export
-  **Chat history** — persistent, clearable, exportable
-  **API key** securely loaded from `.env` file

---

##  Tech Stack

- **Language:** Python 3.9+
- **Frontend:** Streamlit
- **AI Provider:** OpenRouter API (GPT-3.5-Turbo)
- **HTTP Client:** `requests`
- **Config:** `python-dotenv`

---

##  Project Structure

```
AI-Code-Assistant/
├── app.py                    # Streamlit UI (entry point)
├── src/
│   ├── config.py             # Environment, paths, logging
│   ├── prompts.py            # AI prompt templates
│   ├── offline.py            # Offline fallback engine
│   ├── ai_service.py         # AI service layer (API + offline)
│   └── utils.py              # File I/O, history, export utilities
├── data/                     # Chat history storage
├── logs/                     # Application logs
├── screenshots/              # UI screenshots
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── FEATURES.md
├── ARCHITECTURE.md
└── CONTRIBUTING.md
```

---

##  Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-code-assistant.git
cd ai-code-assistant

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Linux/Mac
# OR
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your OpenRouter API key
#    Copy .env.example to .env and paste your key:
cp .env.example .env
# Edit .env and set: OPENROUTER_API_KEY=sk-or-...

# 5. Run the app
streamlit run app.py
```

> **No API key? No problem!** The app automatically falls back to offline mode with template-based responses.

### Get a Free API Key

1. Visit [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up / log in
3. Create a new API key
4. Paste it into your `.env` file

---

##  Usage

### Online Mode (API Key Set)

1. Launch the app with `streamlit run app.py`
2. The app automatically detects your API key
3. Use any feature — all responses come from GPT-3.5 via OpenRouter
4. Chat history is preserved across sessions

### Offline Mode (No API Key)

1. Launch the app — you'll see a banner indicating offline mode
2. All 6 features work with template-based responses:
   - **Generate:** Templates for prime, palindrome, fibonacci, factorial, sorting, fizzbuzz
   - **Explain:** Identifies functions, classes, loops, conditionals
   - **Debug:** Tips for 10+ common Python exceptions
   - **Improve:** Adds PEP 8 suggestions
   - **Comment:** Inserts standard comments
   - **Chat:** General help messages
3. Add an API key anytime via the sidebar to switch to online mode

---

##  Screenshots

> *Screenshots go here. Replace these placeholders with actual images from `screenshots/`.*

| Feature | Preview |
|---------|---------|
| Generate Code | `screenshots/generate.png` |
| Explain Code | `screenshots/explain.png` |
| Debug Error | `screenshots/debug.png` |
| AI Chat | `screenshots/chat.png` |

---

##  Architecture

```
app.py (Streamlit UI)
    │
    ▼
ai_service.py (AI Service Layer)
    │
    ├── Online: OpenRouter API (GPT-3.5)
    └── Offline: offline.py (templates)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the complete architecture breakdown.

---

##  Future Enhancements

- [ ]  **Syntax highlighting** in chat responses
- [ ]  **Multiple AI providers** (OpenAI, Anthropic, Google)
- [ ]  **Custom model selection** dropdown
- [ ]  **History search** across past conversations
- [ ]  **Code execution sandbox** (run generated code safely)
- [ ]  **Export as PDF**
- [ ]  **Multi-language support** (JavaScript, Java, C++)
- [ ]  **Docker support** for easy deployment
- [ ]  **Dark/light theme toggle** within the app
- [ ]  **Unit tests** for all modules

---

##  License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

##  Contributors

- **Your Name** — *Initial work* — [@yourusername](https://github.com/yourusername)

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

<div align="center">
  <sub>Built with  by a Python enthusiast · College Minor Project · 2026</sub>
</div>