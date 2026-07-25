"""Prompt templates for AI tasks."""


SYSTEM_PROMPT = (
    "You are VisionCode AI, an expert Python and Computer Vision engineering assistant. "
    "You specialize in clean code, algorithmic optimization, image processing, OpenCV, "
    "Pillow, and deep learning in computer vision. "
    "Provide clean, PEP 8-compliant, beginner-friendly answers with working code examples. "
    "Be concise, accurate, and helpful."
)


def generate_code_prompt(problem: str) -> str:
    """Return the prompt for code generation."""
    return f"""
You are an expert Python and Computer Vision programmer.
Write clean, beginner-friendly Python code that solves the problem below.

Problem:
{problem}

Return ONLY the Python code inside a single code block. Add brief comments.
"""


def explain_code_prompt(code: str) -> str:
    """Return the prompt for code explanation."""
    return f"""
Explain the following Python code step by step for a beginner.

Keep it simple. Describe:
1. What the code does overall
2. Each line or block — what it does and why

Code:
{code}
"""


def debug_error_prompt(error: str) -> str:
    """Return the prompt for debugging an error."""
    return f"""
You are a Python and Computer Vision debugging expert.
Analyze the error below, explain its cause, and provide a corrected version.

Error / Code:
{error}

Include:
- Root cause
- How to fix it
- Corrected code (if applicable)
"""


def improve_code_prompt(code: str) -> str:
    """Return the prompt for code improvement."""
    return f"""
Improve the Python code below. Focus on:
- Readability (descriptive names, consistent style)
- Performance (avoid unnecessary work)
- Maintainability (modularity, DRY)
- Best practices (PEP 8)

Return the improved code with a short summary of changes.

Code:
{code}
"""


def add_comments_prompt(code: str) -> str:
    """Return the prompt for adding comments."""
    return f"""
Add clear, helpful comments to the Python code below.
Explain what each section does without being overly verbose.

Return the full code with comments added.

Code:
{code}
"""


def chat_prompt(message: str) -> str:
    """Return the prompt for a general chat message."""
    return message


def vision_analyze_prompt(user_question: str) -> str:
    """Return the prompt for analyzing an uploaded image with a coding question."""
    return f"""
You are VisionCode AI, a multi-modal computer vision and Python assistant.
Examine this image and address the user's request:

"{user_question}"

If the image is a code screenshot, extract the code, explain it, and fix any errors.
If it is a system diagram or architectural diagram, explain the components and how to model it in Python.
If it is a UI wireframe, describe the layout and write Streamlit or Tkinter Python code to build it.
Provide clean, working, and well-commented code blocks where appropriate.
"""