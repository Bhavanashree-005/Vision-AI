"""AI-powered Python Code Assistant CLI.

This project provides a simple command-line assistant for:
- generating Python code from a problem statement
- explaining Python code
- debugging errors
- improving code quality
- adding comments to code
- chatting with an AI assistant

It works with the OpenRouter API when an API key is available,
and falls back to built-in sample responses when no key is configured.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

try:
    import requests
except ImportError:  # pragma: no cover - depends on environment
    requests = None

try:
    from getpass import getpass
except ImportError:  # pragma: no cover
    getpass = None

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "chat_history.json"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_history() -> List[Dict[str, str]]:
    if HISTORY_FILE.exists():
        try:
            with HISTORY_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
    return [
        {
            "role": "system",
            "content": (
                "You are a helpful Python coding assistant. "
                "Provide clean, beginner-friendly answers and code examples."
            ),
        }
    ]


def save_history(history: List[Dict[str, str]]) -> None:
    with HISTORY_FILE.open("w", encoding="utf-8") as handle:
        json.dump(history, handle, indent=2)


def get_api_key() -> Optional[str]:
    key = os.getenv("OPENROUTER_API_KEY") or os.getenv("AI_API_KEY")
    if key:
        return key

    if getpass is not None:
        try:
            value = getpass("Enter OpenRouter API key (leave blank to use offline mode): ")
        except Exception:
            value = ""
        return value.strip() or None
    return None


def fallback_response(task: str, user_input: str) -> str:
    if task == "generate":
        return (
            "# Offline fallback response\n"
            "def is_even(number):\n"
            "    return number % 2 == 0\n\n"
            "print(is_even(10))\n"
        )

    if task == "explain":
        return (
            "This is an offline fallback explanation. "
            "The program uses a loop to repeat actions and print values."
        )

    if task == "debug":
        return (
            "Offline fallback: check the spelling of the variable or function name, "
            "and verify that the object exists before using it."
        )

    if task == "improve":
        return (
            "Offline fallback: use descriptive variable names, avoid repeated code, "
            "and keep the logic simple and readable."
        )

    if task == "comment":
        return (
            "# Offline fallback: add short comments to explain the purpose of each section."
        )

    if task == "chat":
        return "Offline fallback: I can help you write, explain, debug, and improve Python code."

    return "Offline fallback: no AI response was generated."


def ask_ai(task: str, user_input: str, history: List[Dict[str, str]]) -> str:
    api_key = get_api_key()
    if not api_key or requests is None:
        return fallback_response(task, user_input)

    messages = [history[0]] + history[1:]
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
    except Exception:
        answer = fallback_response(task, user_input)

    history.append({"role": "assistant", "content": answer})
    save_history(history)
    return answer


def generate_code(problem: str, history: List[Dict[str, str]]) -> str:
    prompt = f"""
You are an expert Python programmer.
Write clean, beginner-friendly Python code.

Problem:
{problem}

Only return Python code.
"""
    return ask_ai("generate", prompt, history)


def explain_code(code: str, history: List[Dict[str, str]]) -> str:
    prompt = f"""
Explain the following Python code line by line for a beginner.

Code:
{code}
"""
    return ask_ai("explain", prompt, history)


def debug_error(error: str, history: List[Dict[str, str]]) -> str:
    prompt = f"""
You are a Python debugging expert.
Explain what caused the error, how to fix it, and show corrected code if possible.

Error:
{error}
"""
    return ask_ai("debug", prompt, history)


def improve_code(code: str, history: List[Dict[str, str]]) -> str:
    prompt = f"""
Improve the following Python code to make it cleaner, faster, and more readable.

Code:
{code}
"""
    return ask_ai("improve", prompt, history)


def add_comments(code: str, history: List[Dict[str, str]]) -> str:
    prompt = f"""
Add clear comments to the following Python code.

Code:
{code}
"""
    return ask_ai("comment", prompt, history)


def chat_session(history: List[Dict[str, str]]) -> None:
    print("\nAI Code Assistant Chat")
    print("Type 'exit' to leave the chat.\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": question})
        answer = ask_ai("chat", question, history)
        print("\nAssistant:")
        print(answer)
        print()


def interactive_menu(history: List[Dict[str, str]]) -> None:
    while True:
        print("\n===== AI CODE ASSISTANT =====")
        print("1. Generate Code")
        print("2. Explain Code")
        print("3. Debug Error")
        print("4. Improve Code")
        print("5. Add Comments")
        print("6. Chat")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            problem = input("Describe the problem: ")
            print(generate_code(problem, history))
        elif choice == "2":
            code = input("Paste Python code:\n")
            print(explain_code(code, history))
        elif choice == "3":
            error = input("Paste the error:\n")
            print(debug_error(error, history))
        elif choice == "4":
            code = input("Paste Python code:\n")
            print(improve_code(code, history))
        elif choice == "5":
            code = input("Paste Python code:\n")
            print(add_comments(code, history))
        elif choice == "6":
            chat_session(history)
        elif choice == "7":
            break
        else:
            print("Please choose a valid option.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-powered Python Code Assistant")
    parser.add_argument("command", nargs="?", choices=["generate", "explain", "debug", "improve", "comment", "chat", "menu"], help="Action to run")
    parser.add_argument("value", nargs="?", help="Input text or code")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    history = load_history()

    if args.command is None:
        interactive_menu(history)
        return

    if args.command == "menu":
        interactive_menu(history)
        return

    if not args.value:
        parser.error("A value is required for this command")

    if args.command == "generate":
        print(generate_code(args.value, history))
    elif args.command == "explain":
        print(explain_code(args.value, history))
    elif args.command == "debug":
        print(debug_error(args.value, history))
    elif args.command == "improve":
        print(improve_code(args.value, history))
    elif args.command == "comment":
        print(add_comments(args.value, history))
    elif args.command == "chat":
        chat_session(history)


if __name__ == "__main__":
    main()


