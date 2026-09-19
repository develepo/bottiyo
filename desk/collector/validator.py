from __future__ import annotations

from .models import (
    CandidateStatus,
    SongCandidate,
    ValidationResult,
)


class CandidateValidator:

    def validate(
        self,
        candidate: SongCandidate,
    ) -> ValidationResult:

        if not candidate.post_id:
            return ValidationResult(
                CandidateStatus.REJECTED,
                "missing_post_id",
            )

        if not candidate.source_url:
            return ValidationResult(
                CandidateStatus.REJECTED,
                "missing_source_url",
            )

        if not candidate.image_url and not candidate.image_path:
            return ValidationResult(
                CandidateStatus.REJECTED,
                "missing_image",
            )

        if not candidate.song_title:
            return ValidationResult(
                CandidateStatus.REJECTED,
                "missing_song_title",
            )

        if not candidate.artist:
            return ValidationResult(
                CandidateStatus.REJECTED,
                "missing_artist",
            )

        return ValidationResult(
            CandidateStatus.VALID
        )