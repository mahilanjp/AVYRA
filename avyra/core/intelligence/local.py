import subprocess
from pathlib import Path
from typing import Any

from avyra.core.intelligence.provider import (
    IntelligenceProvider,
    IntelligenceResult,
)


class LocalIntelligence(IntelligenceProvider):
    """AVYRA's local model-backed intelligence runtime."""

    SYSTEM_PROMPT = """
You are AVYRA — Adaptive Voice, Yielding Reasoning & Automation.

You are a female personal AI assistant.
The user is your boss and owner.

Be natural, intelligent, concise, and friendly.
You can communicate in English, Tamil, Malayalam,
Tanglish, Manglish, and mixed-language conversation.

Never expose private internal reasoning.
Respond with the final useful answer only.
""".strip()

    def __init__(self) -> None:
        self.runtime_path = Path(
            r"C:\Users\MahilanJP\AppData\Local\Microsoft\WinGet\Packages"
            r"\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe"
            r"\llama-cli.exe"
        )

        self.model = "Qwen/Qwen3-4B-GGUF:Q4_K_M"

    def generate(
        self,
        prompt: str,
        context: dict[str, Any] | None = None,
    ) -> IntelligenceResult:

        if not self.runtime_path.exists():
            raise RuntimeError(
                f"AVYRA local runtime not found: {self.runtime_path}"
            )

        full_prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"Boss: {prompt}\n"
            f"AVYRA:"
        )

        command = [
            str(self.runtime_path),
            "-hf",
            self.model,
            "-p",
            full_prompt,
            "-n",
            "256",
            "--single-turn",
            "--reasoning",
            "off",
            "--no-display-prompt",
        ]

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                "AVYRA local intelligence timed out."
            ) from exc

        if process.returncode != 0:
            raise RuntimeError(
                f"AVYRA local intelligence failed:\n{process.stderr}"
            )

        output = process.stdout.strip()

        return IntelligenceResult(
            text=output,
            metadata={
                "engine": "avyra-local",
                "model": self.model,
                "status": "ready",
            },
        )