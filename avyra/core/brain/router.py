from avyra.core.intelligence.provider import IntelligenceProvider
from avyra.core.models import AVYRARequest, AVYRAResponse, Intent


class BrainRouter:
    """Routes requests through AVYRA's intelligence and capabilities."""

    def __init__(self, intelligence: IntelligenceProvider) -> None:
        self.intelligence = intelligence

    def route(self, request: AVYRARequest) -> AVYRAResponse:
        request.intent = Intent.CONVERSATION

        result = self.intelligence.generate(
            prompt=request.text,
            context={
                "language": request.language,
                "entities": request.entities,
            },
        )

        return AVYRAResponse(
            text=result.text,
            source="intelligence",
            request_id=request.request_id,
            metadata={
                "intent": request.intent.value,
                "language": request.language,
                **result.metadata,
            },
        )