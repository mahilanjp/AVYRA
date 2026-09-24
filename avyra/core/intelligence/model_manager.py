from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModelInfo:
    name: str
    path: Path
    model_type: str
    enabled: bool = True


class ModelManager:
    """Manages models owned and used by AVYRA."""

    def __init__(self, models_dir: str = "models") -> None:
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def list_models(self) -> list[ModelInfo]:
        models: list[ModelInfo] = []

        for path in self.models_dir.iterdir():
            if path.is_file():
                models.append(
                    ModelInfo(
                        name=path.stem,
                        path=path,
                        model_type=path.suffix.lower().lstrip("."),
                    )
                )

        return models