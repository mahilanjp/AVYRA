import subprocess
import time
import urllib.request
from pathlib import Path


class RuntimeManager:
    """Starts and manages AVYRA's persistent local inference runtime."""

    def __init__(self) -> None:
        self.runtime_path = Path(
            r"C:\Users\MahilanJP\AppData\Local\Microsoft\WinGet\Packages"
            r"\ggml.llamacpp_Microsoft.Winget.Source_8wekyb3d8bbwe"
            r"\llama-server.exe"
        )

        self.model = "Qwen/Qwen3-4B-GGUF:Q4_K_M"
        self.host = "127.0.0.1"
        self.port = 8080
        self.process: subprocess.Popen | None = None

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def start(self) -> None:
        if self.is_ready():
            return

        if not self.runtime_path.exists():
            raise RuntimeError(
                f"AVYRA runtime not found: {self.runtime_path}"
            )

        command = [
            str(self.runtime_path),
            "--hf-repo",
            self.model,
            "--host",
            self.host,
            "--port",
            str(self.port),
            "--alias",
            "avyra-local",
            "--reasoning",
            "off",
        ]

        creation_flags = getattr(
            subprocess,
            "CREATE_NO_WINDOW",
            0,
        )

        self.process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags,
        )

        self._wait_until_ready()

    def is_ready(self) -> bool:
        try:
            with urllib.request.urlopen(
                f"{self.base_url}/health",
                timeout=1,
            ) as response:
                return response.status == 200
        except Exception:
            return False

    def _wait_until_ready(self, timeout: int = 120) -> None:
        deadline = time.time() + timeout

        while time.time() < deadline:
            if self.is_ready():
                return

            if self.process and self.process.poll() is not None:
                raise RuntimeError(
                    "AVYRA intelligence runtime stopped unexpectedly."
                )

            time.sleep(0.5)

        self.stop()
        raise RuntimeError(
            "Timed out while loading AVYRA's local intelligence."
        )

    def stop(self) -> None:
        if self.process is None:
            return

        if self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()

        self.process = None