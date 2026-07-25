"""AI service layer — handles API communication and offline fallback."""

from __future__ import annotations

from typing import Optional

import requests

from src.config import (
    DEFAULT_MODEL,
    OPENROUTER_URL,
    REQUEST_TIMEOUT,
    SITE_NAME,
    SITE_URL,
    get_api_key,
    logger,
)
from src.offline import handle_offline
from src.prompts import (
    SYSTEM_PROMPT,
    add_comments_prompt,
    chat_prompt,
    debug_error_prompt,
    explain_code_prompt,
    generate_code_prompt,
    improve_code_prompt,
    vision_analyze_prompt,
)
from src.utils import load_history, save_history


class AIService:
    """Handles AI communication with OpenRouter API and offline fallback."""

    def __init__(self) -> None:
        self.history: list[dict[str, str]] = load_history()
        self._api_key: Optional[str] = get_api_key()

    # ------------------------------------------------------------------
    # API key management
    # ------------------------------------------------------------------

    @property
    def has_api_key(self) -> bool:
        """Check if an API key is configured."""
        return bool(self._api_key)

    def update_api_key(self, key: str) -> None:
        """Set a new API key and configure it in the environment."""
        from src.config import set_api_key
        self._api_key = key.strip()
        set_api_key(key)
        logger.info("API key updated.")

    # ------------------------------------------------------------------
    # Core AI call
    # ------------------------------------------------------------------

    def ask(
        self,
        task: str,
        user_input: str,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        image_mime: str = "image/jpeg",
    ) -> str:
        """Send a prompt to the AI or use offline fallback.

        Args:
            task: Task identifier (generate, explain, debug, vision, etc.).
            user_input: Raw input from the user.
            prompt: The formatted prompt to send.
            image_bytes: Optional raw bytes of an image.
            image_mime: MIME type of the image.

        Returns:
            AI response text.
        """
        if not self._api_key:
            logger.info("No API key — using offline mode for task '%s'.", task)
            return self._offline_response(task, user_input, image_bytes=image_bytes)

        try:
            return self._call_api(prompt, image_bytes, image_mime)
        except requests.RequestException as exc:
            logger.error("API request failed: %s. Switching to offline mode.", exc)
            return self._offline_response(task, user_input, image_bytes=image_bytes)
        except Exception as exc:
            logger.error("Unexpected API error: %s. Switching to offline mode.", exc)
            return self._offline_response(task, user_input, image_bytes=image_bytes)

    def _call_api(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        image_mime: str = "image/jpeg",
    ) -> str:
        """Make the actual HTTP call to OpenRouter."""
        messages = [self.history[0]] + self.history[1:]

        if image_bytes:
            import base64
            b64_data = base64.b64encode(image_bytes).decode("utf-8")
            content = [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{image_mime};base64,{b64_data}"},
                },
            ]
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": SITE_URL,
            "X-Title": SITE_NAME,
        }

        payload = {
            "model": DEFAULT_MODEL,
            "messages": messages,
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        self.history.append({"role": "assistant", "content": answer})
        save_history(self.history)
        return answer

    def _offline_response(self, task: str, user_input: str, image_bytes: Optional[bytes] = None) -> str:
        """Get a response from the offline engine."""
        return handle_offline(task, user_input, image_bytes=image_bytes)

    # ------------------------------------------------------------------
    # Task-specific methods
    # ------------------------------------------------------------------

    def generate_code(self, problem: str) -> str:
        """Generate Python code from a problem description."""
        prompt = generate_code_prompt(problem)
        return self.ask("generate", problem, prompt)

    def explain_code(self, code: str) -> str:
        """Explain the given Python code."""
        prompt = explain_code_prompt(code)
        return self.ask("explain", code, prompt)

    def debug_error(self, error: str) -> str:
        """Debug a Python error and suggest fixes."""
        prompt = debug_error_prompt(error)
        return self.ask("debug", error, prompt)

    def improve_code(self, code: str) -> str:
        """Suggest improvements for the given code."""
        prompt = improve_code_prompt(code)
        return self.ask("improve", code, prompt)

    def add_comments(self, code: str) -> str:
        """Add comments to the given code."""
        prompt = add_comments_prompt(code)
        return self.ask("comment", code, prompt)

    def chat(self, message: str) -> str:
        """General AI chat."""
        prompt = chat_prompt(message)
        self.history.append({"role": "user", "content": message})
        answer = self.ask("chat", message, prompt)
        if answer:
            self.history.append({"role": "assistant", "content": answer})
            save_history(self.history)
        return answer

    def vision_analyze(self, question: str, image_bytes: bytes, image_mime: str = "image/jpeg") -> str:
        """Analyze an image using multi-modal AI vision."""
        prompt = vision_analyze_prompt(question)
        return self.ask("vision", question, prompt, image_bytes=image_bytes, image_mime=image_mime)

    # ------------------------------------------------------------------
    # History management
    # ------------------------------------------------------------------

    def reset_history(self) -> None:
        """Clear conversation history."""
        from src.utils import clear_history as _clear
        _clear()
        from src.utils import _default_history
        self.history = _default_history()
        logger.info("Chat history reset in memory.")

    def get_exports(self) -> str:
        """Return the chat history formatted for export."""
        from src.utils import export_chat_history
        return export_chat_history(self.history)