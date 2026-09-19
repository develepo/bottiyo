from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CandidateStatus(str, Enum):
    VALID = "valid"
    REJECTED = "rejected"
    ERROR = "error"


@dataclass(slots=True)
class SongCandidate:
    post_id: str
    source_url: str

    image_url: str | None = None
    image_path: str | None = None

    song_id: str | None = None
    song_title: str | None = None
    artist: str | None = None
    language: str | None = None

    why: str | None = None

    raw_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ValidationResult:
    status: CandidateStatus
    reason: str | None = None

    @property
    def valid(self) -> bool:
        return self.status == CandidateStatus.VALID