from avyra.core.models import AVYRARequest


class NLPProcessor:
    """Transforms raw input into AVYRA's normalized request format."""

    def process(self, text: str) -> AVYRARequest:
        cleaned_text = text.strip()

        if not cleaned_text:
            raise ValueError("Input cannot be empty.")

        return AVYRARequest(
            text=cleaned_text,
            language=self._detect_script(cleaned_text),
        )

    def _detect_script(self, text: str) -> str:
        """
        First-pass script detection.

        Romanized Tamil/Malayalam requires semantic language detection,
        which will be handled by AVYRA's AI NLP layer.
        """

        has_tamil = any("\u0B80" <= char <= "\u0BFF" for char in text)
        has_malayalam = any("\u0D00" <= char <= "\u0D7F" for char in text)

        if has_tamil and has_malayalam:
            return "multilingual"

        if has_tamil:
            return "ta"

        if has_malayalam:
            return "ml"

        # Latin script alone cannot reliably distinguish:
        # English / Tanglish / Manglish / code-switching.
        return "latin-undetermined"