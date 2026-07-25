#  Contributing

Thank you for your interest in contributing to the AI Code Assistant!

## How to Contribute

1. **Fork** the repository
2. **Clone** your fork
3. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
4. **Commit** your changes (`git commit -m 'Add amazing feature'`)
5. **Push** to the branch (`git push origin feature/amazing-feature`)
6. Open a **Pull Request**

## Development Setup

```bash
git clone https://github.com/yourusername/ai-code-assistant.git
cd ai-code-assistant
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Code Style

- Follow **PEP 8** conventions
- Use **type hints** for all function signatures
- Write **docstrings** for public functions and classes
- Keep functions **small and focused** (single responsibility)
- Add **meaningful variable names** — avoid abbreviations

## Pull Request Checklist

- [ ] Code compiles without errors
- [ ] Follows PEP 8 style
- [ ] Includes docstrings for new public functions
- [ ] No duplicate code (check `offline.py` for similar patterns)
- [ ] Tested with both API key set and unset
- [ ] README updated if adding a feature

## Reporting Issues

Open an issue with:
- A clear title and description
- Steps to reproduce (if bug)
- Expected vs actual behaviour
- Screenshots (if applicable)

## Code of Conduct

Be respectful, inclusive, and constructive. We welcome contributors of all skill levels.