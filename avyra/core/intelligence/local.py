from typing import Any

from avyra.core.intelligence.provider import (
    IntelligenceProvider,
    IntelligenceResult,
)


class LocalIntelligence(IntelligenceProvider):
    """
    AVYRA's local intelligence runtime.

    The native model/inference implementation will be connected here.
    """

    def generate(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> IntelligenceResult:

        return IntelligenceResult(
            text=f"Local intelligence received: {prompt}",
            metadata={
                "engine": "avyra-local",
                "status": "prototype",
            },
        )