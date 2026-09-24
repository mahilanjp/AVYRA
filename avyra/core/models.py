from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class Intent(str, Enum):
    CONVERSATION = "conversation"
    MEMORY = "memory"
    WEB_SEARCH = "web_search"
    AUTOMATION = "automation"
    CODING = "coding"
    DEVICE = "device"
    VEHICLE = "vehicle"
    UNKNOWN = "unknown"


@dataclass
class AVYRARequest:
    text: str
    intent: Intent = Intent.UNKNOWN
    language: str = "unknown"
    entities: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class AVYRAResponse:
    text: str
    source: str
    request_id: str
    metadata: dict[str, Any] = field(default_factory=dict)