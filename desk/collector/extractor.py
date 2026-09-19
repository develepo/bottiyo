from __future__ import annotations

from .models import SongCandidate
from .source import RawCandidate


class CandidateExtractor:
    """
    Converts source-specific raw candidates into Tuneez candidates.
    """

    def extract(
        self,
        raw: RawCandidate,
    ) -> SongCandidate:

        metadata = raw.raw_metadata

        return SongCandidate(
            post_id=raw.post_id,
            source_url=raw.source_url,
            image_url=raw.image_url,
            song_id=metadata.get("song_id"),
            song_title=metadata.get("song_title"),
            artist=metadata.get("artist"),
            language=metadata.get("language"),
            why=metadata.get("why"),
            raw_metadata=metadata,
        )