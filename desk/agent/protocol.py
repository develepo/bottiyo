from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentTask:
    task_id: str
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentEvent:
    task_id: str
    type: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)