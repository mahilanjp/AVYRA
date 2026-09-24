from avyra.core.brain.router import BrainRouter
from avyra.core.intelligence.local import LocalIntelligence
from avyra.core.models import AVYRAResponse
from avyra.core.nlp.processor import NLPProcessor


class AVYRACore:
    """Central orchestrator for AVYRA."""

    def __init__(self) -> None:
        self.nlp = NLPProcessor()

        self.intelligence = LocalIntelligence()

        self.router = BrainRouter(
            intelligence=self.intelligence,
        )

    def handle(self, text: str) -> AVYRAResponse:
        request = self.nlp.process(text)
        return self.router.route(request)

    def shutdown(self) -> None:
        self.intelligence.shutdown()