from dataclasses import dataclass


@dataclass
class ConversationMessage:
    role: str
    content: str


class ConversationContext:
    """AVYRA's temporary in-session conversation memory."""

    def __init__(self, max_messages: int = 12) -> None:
        self.max_messages = max_messages
        self.messages: list[ConversationMessage] = []

    def add_user(self, text: str) -> None:
        self._add("user", text)

    def add_assistant(self, text: str) -> None:
        self._add("assistant", text)

    def _add(self, role: str, content: str) -> None:
        self.messages.append(
            ConversationMessage(
                role=role,
                content=content,
            )
        )

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def as_api_messages(self) -> list[dict[str, str]]:
        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in self.messages
        ]

    def clear(self) -> None:
        self.messages.clear()