from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntelligenceResult:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class IntelligenceProvider(ABC):
    """Interface implemented by every AVYRA intelligence engine."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> IntelligenceResult:
        raise NotImplementedError