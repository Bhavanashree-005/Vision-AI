#  Feature List

## Core Functionalities

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Generate Code** | Describe a problem and get clean, beginner-friendly Python code |
| 2 | **Explain Code** | Paste Python code and receive a step-by-step explanation |
| 3 | **Debug Error** | Paste an error message and get the root cause + fix |
| 4 | **Improve Code** | Get refactored code with better readability and performance |
| 5 | **Add Comments** | Automatically add meaningful comments to your code |
| 6 | **AI Chat** | Ask general Python questions in a conversational interface |

##  AI Capabilities

- Powered by **OpenRouter API** (GPT-3.5/4 models)
- **Automatic offline fallback** — no API key, no problem
- Template-based offline generation for common problems (fibonacci, palindrome, sorting, etc.)
- Offline debugging tips for 10+ common Python exception types

## ‎ User Interface

- **Streamlit** web app — runs in your browser
- **Sidebar navigation** for all features
- **Large text areas** for code input
- **Syntax-highlighted output** panels
- **Copy to clipboard** button
- **Download response** as .txt file
- **Dark/light theme** compatibility (follows system / Streamlit settings)

##  Data & Persistence

- **Chat history** saved across sessions
- **Clear history** button
- **Export chat** to plain text
- **Read code from `.py` file** upload
- **Save AI responses** automatically to `data/` directory
- **Error logging** to `logs/app.log`

##  Security

- API key stored in `.env` file (loaded via `python-dotenv`)
- Key input uses password masking in UI
- `.env` excluded from version control

## ⚙️ Offline Mode (No API Key Required)

- Generate generic Python templates (prime, palindrome, fibonacci, factorial, sorting, fizzbuzz)
- Explain code structure (identifies functions, classes, loops, conditionals)
- Debugging suggestions for common errors (SyntaxError, NameError, TypeError, etc.)
- Improve code readability with PEP 8 suggestions
- Add standard comments to code sections

##  Performance

- Lightweight — no ML models, no heavy dependencies
- Fast offline responses
- Configurable API timeout (30s default)
- Responsive layout (works on desktop & tablet)