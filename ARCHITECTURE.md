#  Project Architecture

## High-Level Overview

```
┌──────────────────────────────────────────────────────────┐
│                    User (Browser)                        │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                   app.py (Streamlit UI)                  │
│  · Navigation sidebar         · Input / Output panels   │
│  · Chat interface             · File upload             │
│  · Copy / Download buttons    · Error/success messages  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              src/ai_service.py (AI Service Layer)        │
│  · API key management           · History management     │
│  · API communication            · Offline fallback       │
│  · Task dispatch (generate, explain, debug, etc.)        │
└──────┬─────────────────────────────────────┬─────────────┘
       │                                     │
       ▼                                     ▼
┌──────────────┐                  ┌──────────────────────┐
│  OpenRouter  │                  │  src/offline.py       │
│  API         │                  │  · Templates          │
│  (GPT-3.5)   │                  │  · Debug tips         │
│              │                  │  · Code comments      │
└──────────────┘                  │  · Explanations       │
                                 └──────────────────────┘
```

## Directory Structure

```
AI-Code-Assistant/
├── app.py                    # Streamlit frontend (entry point)
├── src/
│   ├── __init__.py
│   ├── config.py             # Paths, env vars, logging, constants
│   ├── prompts.py            # AI prompt templates
│   ├── offline.py            # Offline fallback engine
│   ├── ai_service.py         # AI service layer (API + fallback)
│   └── utils.py              # Utilities (file I/O, history, export)
├── data/
│   ├── .gitkeep
│   └── chat_history.json     # Persisted conversation history
├── logs/
│   ├── .gitkeep
│   └── app.log               # Application logs
├── screenshots/              # Screenshots (for README)
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── FEATURES.md
├── ARCHITECTURE.md
└── CONTRIBUTING.md
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `app.py` | Streamlit UI — all user-facing screens, input, output, navigation |
| `src/config.py` | Environment loading, path constants, logging config, API key helpers |
| `src/prompts.py` | System prompt + task-specific prompt builders |
| `src/offline.py` | Full offline fallback: code templates, debug tips, code comments |
| `src/ai_service.py` | `AIService` class — API calls, offline dispatch, history management |
| `src/utils.py` | Chat history load/save/clear, file read, response export, text helpers |

## Data Flow (Online Mode)

```
1. User enters code/problem in app.py
2. app.py calls AIService.method() (e.g. generate_code)
3. AIService builds prompt via prompts.py
4. AIService calls _call_api(prompt) → HTTP POST to OpenRouter
5. Response parsed → appended to history → saved via utils.py
6. Response returned to app.py → displayed in output panel
```

## Data Flow (Offline Mode)

```
1. User enters code/problem in app.py
2. app.py calls AIService.method()
3. AIService detects no API key → calls _offline_response()
4. offline.py handler matched by task type → generates response
5. Response returned to app.py → displayed in output panel
```

## Design Decisions

- **No ML models** — keeps the project lightweight and dependency-free beyond what's needed for the UI and HTTP calls.
- **Streamlit over Flask/Django** — faster to prototype, built-in widgets for text areas, code blocks, file upload, and state management.
- **Single `AIService` class** — encapsulates all AI logic (both online and offline) behind a clean interface so the UI never deals with API details.
- **Modular prompts** — prompt templates live in their own file so they can be tuned without touching any logic code.
- **Offline engine** — pattern-matches user input against common problem keywords to return useful templates, making the app functional even without internet access.