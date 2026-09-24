import json
import urllib.request
from typing import Any

from avyra.core.intelligence.conversation import ConversationContext
from avyra.core.intelligence.provider import (
    IntelligenceProvider,
    IntelligenceResult,
)
from avyra.core.intelligence.runtime_manager import RuntimeManager


class LocalIntelligence(IntelligenceProvider):
    """AVYRA's persistent local intelligence provider."""

    SYSTEM_PROMPT = """
You are AVYRA — Adaptive Voice, Yielding Reasoning & Automation.

You are a female personal AI assistant.
The user is your boss and owner.

Be natural, intelligent, concise, and friendly.

Understand and respond naturally to:
- English
- Tamil
- Malayalam
- Tanglish
- Manglish
- mixed-language conversation

Never expose private internal reasoning.
Return only the final useful response.
""".strip()

    def __init__(self) -> None:
        self.runtime = RuntimeManager()
        self.runtime.start()
        self.conversation = ConversationContext(max_messages=12)

    def generate(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> IntelligenceResult:

        # Add the boss's message to temporary conversation memory.
        self.conversation.add_user(prompt)

        messages = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT,
            },
            *self.conversation.as_api_messages(),
        ]

        payload = {
            "model": "avyra-local",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 256,
        }

        request = urllib.request.Request(
            f"{self.runtime.base_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=120,
            ) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )
        except Exception as exc:
            raise RuntimeError(
                f"AVYRA intelligence request failed: {exc}"
            ) from exc

        text = result["choices"][0]["message"]["content"].strip()

        # Remember AVYRA's response for the rest of this session.
        self.conversation.add_assistant(text)

        return IntelligenceResult(
            text=text,
            metadata={
                "engine": "avyra-local",
                "model": "Qwen3-4B-Q4_K_M",
                "status": "ready",
            },
        )

    def clear_conversation(self) -> None:
        """Clear AVYRA's temporary conversation memory."""
        self.conversation.clear()

    def shutdown(self) -> None:
        """Stop AVYRA's local intelligence runtime."""
        self.runtime.stop()