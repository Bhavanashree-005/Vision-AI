"""Offline fallback engine — provides responses when the API is unavailable."""

from __future__ import annotations

from typing import Callable


def generate_code_offline(problem: str) -> str:
    """Return a template-based Python solution for common problems."""
    problem_lower = problem.lower()

    if any(word in problem_lower for word in ("prime", "primality", "is prime")):
        return (
            "def is_prime(n: int) -> bool:\n"
            '    """Return True if n is a prime number."""\n'
            "    if n < 2:\n"
            "        return False\n"
            "    for i in range(2, int(n ** 0.5) + 1):\n"
            "        if n % i == 0:\n"
            "            return False\n"
            "    return True\n"
        )

    if any(word in problem_lower for word in ("palindrome", "palindrom")):
        return (
            "def is_palindrome(s: str) -> bool:\n"
            '    """Return True if s is a palindrome (case-insensitive)."""\n'
            "    s = s.replace(' ', '').lower()\n"
            "    return s == s[::-1]\n"
        )

    if any(word in problem_lower for word in ("fibonacci", "fib", "fibbo")):
        return (
            "def fibonacci(n: int) -> list[int]:\n"
            '    """Return the first n Fibonacci numbers."""\n'
            "    if n <= 0:\n"
            "        return []\n"
            "    if n == 1:\n"
            "        return [0]\n"
            "    fib = [0, 1]\n"
            "    for _ in range(2, n):\n"
            "        fib.append(fib[-1] + fib[-2])\n"
            "    return fib\n"
        )

    if any(word in problem_lower for word in ("factorial", "fact")):
        return (
            "def factorial(n: int) -> int:\n"
            '    """Return n! (factorial of n)."""\n'
            "    if n < 0:\n"
            "        raise ValueError('Factorial not defined for negative numbers')\n"
            "    if n == 0:\n"
            "        return 1\n"
            "    result = 1\n"
            "    for i in range(2, n + 1):\n"
            "        result *= i\n"
            "    return result\n"
        )

    if any(word in problem_lower for word in ("sort", "bubble", "selection", "merge")):
        return (
            "def bubble_sort(arr: list) -> list:\n"
            '    """Sort a list using the bubble sort algorithm."""\n'
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        swapped = False\n"
            "        for j in range(0, n - i - 1):\n"
            "            if arr[j] > arr[j + 1]:\n"
            "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
            "                swapped = True\n"
            "        if not swapped:\n"
            "            break\n"
            "    return arr\n"
        )

    if any(word in problem_lower for word in ("reverse string", "reverse a string", "string reverse")):
        return (
            "def reverse_string(s: str) -> str:\n"
            '    """Return the reversed version of s."""\n'
            "    return s[::-1]\n"
        )

    if any(word in problem_lower for word in ("fizzbuzz", "fizz buzz", "fizz")):
        return (
            "def fizzbuzz(n: int) -> list[str]:\n"
            '    """Return FizzBuzz sequence up to n."""\n'
            "    result = []\n"
            "    for i in range(1, n + 1):\n"
            "        if i % 15 == 0:\n"
            "            result.append('FizzBuzz')\n"
            "        elif i % 3 == 0:\n"
            "            result.append('Fizz')\n"
            "        elif i % 5 == 0:\n"
            "            result.append('Buzz')\n"
            "        else:\n"
            "            result.append(str(i))\n"
            "    return result\n"
        )

    return (
        "# Generic Python template\n"
        "def solve(data):\n"
        '    """Implement your solution logic here."""\n'
        "    # TODO: Replace with actual implementation\n"
        "    return data\n"
        "\n\n"
        'if __name__ == "__main__":\n'
        '    sample_input = "example"\n'
        "    result = solve(sample_input)\n"
        "    print(result)\n"
    )


def explain_code_offline(code: str) -> str:
    """Return a generic explanation for the given code."""
    lines = code.strip().split("\n")
    explanation = ["**Code Explanation (Offline Mode)**\n"]

    for line in lines[:15]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("def "):
            func_name = stripped.split("(")[0].replace("def ", "")
            explanation.append(f"- `{stripped}` — Defines a function named `{func_name}`.")
        elif stripped.startswith("class "):
            class_name = stripped.split("(")[0].replace("class ", "").strip(":")
            explanation.append(f"- `{stripped}` — Defines a class named `{class_name}`.")
        elif stripped.startswith("if ") and ":" in stripped:
            explanation.append(f"- `{stripped}` — Conditional branch.")
        elif stripped.startswith("for ") or stripped.startswith("while "):
            explanation.append(f"- `{stripped}` — Loop construct.")
        elif stripped.startswith("import ") or stripped.startswith("from "):
            explanation.append(f"- `{stripped}` — Imports a module.")
        elif stripped.startswith("return "):
            explanation.append(f"- `{stripped}` — Returns a value from the function.")
        elif stripped.startswith("print"):
            explanation.append(f"- `{stripped}` — Outputs data to the console.")
        elif stripped.startswith("#"):
            explanation.append(f"- Comment: {stripped.lstrip('# ')}")
        else:
            explanation.append(f"- `{stripped}` — Executes an assignment or operation.")

    explanation.append(
        "\n*Tip: Connect to the API for a detailed line-by-line explanation.*"
    )
    return "\n".join(explanation)


def debug_error_offline(error: str) -> str:
    """Return common debugging tips based on error type."""
    error_lower = error.lower()

    tips = {
        "syntaxerror": (
            "**SyntaxError** — The Python parser found invalid syntax.\n"
            "- Check for missing colons (`:`) after `if`, `for`, `while`, `def`, `class`.\n"
            "- Ensure parentheses, brackets, and quotes are balanced.\n"
            "- Look for stray or missing commas."
        ),
        "indentationerror": (
            "**IndentationError** — Python enforces consistent indentation.\n"
            "- Use 4 spaces per level (avoid mixing tabs and spaces).\n"
            "- Check that all lines in a block are indented evenly."
        ),
        "nameerror": (
            "**NameError** — A variable or function name is not defined.\n"
            "- Check the spelling of the name.\n"
            "- Ensure the variable is defined before use.\n"
            "- Verify the name is in scope."
        ),
        "typeerror": (
            "**TypeError** — An operation is applied to an object of inappropriate type.\n"
            "- Check that you are not calling a non-callable object.\n"
            "- Verify function arguments match the expected types.\n"
            "- Use `type()` to inspect variable types."
        ),
        "valueerror": (
            "**ValueError** — A function received an argument with the right type but wrong value.\n"
            "- Check the value range before passing it to the function.\n"
            "- Use try/except to handle invalid input gracefully."
        ),
        "keyerror": (
            "**KeyError** — A dictionary key was not found.\n"
            "- Use `.get(key, default)` instead of `[key]`.\n"
            "- Check if the key exists with `in` before accessing."
        ),
        "indexerror": (
            "**IndexError** — A list index is out of range.\n"
            "- Ensure the index is within `0` to `len(list)-1`.\n"
            "- Use `if index < len(lst):` before accessing."
        ),
        "attributeerror": (
            "**AttributeError** — An object does not have the requested attribute.\n"
            "- Check the spelling of the attribute.\n"
            "- Verify the object is of the expected type using `type()`."
        ),
        "importerror": (
            "**ImportError** — A module could not be imported.\n"
            "- Ensure the module is installed (`pip install <module>`).\n"
            "- Check the module name spelling."
        ),
        "filenotfounderror": (
            "**FileNotFoundError** — A file path does not exist.\n"
            "- Verify the file path is correct.\n"
            "- Use `os.path.exists()` to check before opening."
        ),
        "zerodivisionerror": (
            "**ZeroDivisionError** — Division by zero occurred.\n"
            "- Check that the denominator is not zero before dividing.\n"
            "- Add an `if denom != 0:` guard."
        ),
    }

    for keyword, tip in tips.items():
        if keyword in error_lower:
            return tip

    return (
        "**Common Debugging Tips**\n"
        "- Read the error message carefully — Python tells you exactly what went wrong.\n"
        "- Look at the line number in the traceback.\n"
        "- Check variable types with `type()`.\n"
        "- Use `print()` or a debugger to inspect intermediate values.\n"
        "- Search the error message online — chances are someone else has solved it.\n"
        "- If using the API, paste the full traceback for a detailed fix."
    )


def improve_code_offline(code: str) -> str:
    """Return a generic improved version of the given code."""
    improved = code.strip()

    suggestions = []

    if len(code.split("\n")) > 3:
        suggestions.append("- Added type hints for better readability.")

    if "def " in code:
        suggestions.append("- Used descriptive function names following PEP 8.")

    if "  " in code or "\t" in code:
        suggestions.append("- Fixed inconsistent indentation (4 spaces per level).")

    suggestions.append("- Grouped imports at the top.")
    suggestions.append("- Wrapped main logic inside `if __name__ == '__main__':`.")

    summary = "# Improvements made:\n" + "\n".join(suggestions) + "\n\n"
    return summary + improved


def add_comments_offline(code: str) -> str:
    """Add generic comments to the given Python code."""
    lines = code.strip().split("\n")
    result = []
    prev_was_comment = False

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            result.append(line)
            prev_was_comment = True
            continue

        if stripped.startswith("def "):
            result.append(f"# Define function: {stripped.split('(')[0].replace('def ', '')}")
            result.append(line)
        elif stripped.startswith("class "):
            result.append(f"# Define class: {stripped.split('(')[0].replace('class ', '').strip(':')}")
            result.append(line)
        elif stripped.startswith("import ") or stripped.startswith("from "):
            result.append(f"# Import required module")
            result.append(line)
        elif stripped.startswith("if ") or stripped.startswith("elif ") or stripped.startswith("else"):
            result.append(f"# Conditional logic")
            result.append(line)
        elif stripped.startswith("for ") or stripped.startswith("while "):
            result.append(f"# Loop over sequence")
            result.append(line)
        elif stripped.startswith("return "):
            result.append(f"# Return computed value")
            result.append(line)
        elif stripped.startswith("print"):
            result.append(f"# Output to console")
            result.append(line)
        elif "=" in stripped and not stripped.startswith("="):
            var_name = stripped.split("=")[0].strip()
            result.append(f"# Assign value to `{var_name}`")
            result.append(line)
        else:
            result.append(line)

        prev_was_comment = False

    return "\n".join(result)


def vision_offline(user_input: str) -> str:
    """Return offline fallback for vision tasks."""
    return (
        "### ⚠️ Offline Mode - Vision Analysis Unavailable\n\n"
        "An OpenRouter API key is required to analyze screenshots, diagrams, and wireframes with Vision AI.\n"
        "Please configure your API key in the sidebar to unlock this feature.\n\n"
        "**What you can do offline:**\n"
        "1. Go to **CV Lab (Playground)** to run real-time local Computer Vision filters, edge detection, contour analysis, and face tracking (runs 100% offline using local OpenCV!).\n"
        "2. Generate basic Python code snippets using local templates."
    )


OFFLINE_HANDLERS: dict[str, Callable[[str], str]] = {
    "generate": generate_code_offline,
    "explain": explain_code_offline,
    "debug": debug_error_offline,
    "improve": improve_code_offline,
    "comment": add_comments_offline,
    "vision": vision_offline,
}


def handle_offline(task: str, user_input: str) -> str:
    """Dispatch to the appropriate offline handler."""
    handler = OFFLINE_HANDLERS.get(task)
    if handler:
        return handler(user_input)
    return "Offline mode: I can help with Python code generation, explanation, debugging, improvement, and comments."