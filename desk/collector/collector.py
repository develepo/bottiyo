from __future__ import annotations

from dataclasses import dataclass

from .dataset import DatasetWriter
from .extractor import CandidateExtractor
from .models import CandidateStatus
from .source import BrowserSource


@dataclass(slots=True)
class CollectionStats:
    observed: int = 0
    valid: int = 0
    rejected: int = 0
    errors: int = 0


class CollectionAgent:

    def __init__(
        self,
        source: BrowserSource,
        writer: DatasetWriter,
        extractor: CandidateExtractor | None = None,
    ) -> None:
        self.source = source
        self.writer = writer
        self.extractor = extractor or CandidateExtractor()

        self.stats = CollectionStats()

        self._seen: set[str] = set()

    def collect(
        self,
        target: int,
    ) -> CollectionStats:

        if target <= 0:
            raise ValueError("target must be greater than zero")

        while self.stats.valid < target:

            raw_candidates = self.source.observe()

            if not raw_candidates:
                self.stats.errors += 1
                self.source.next()
                continue

            progressed = False

            for raw in raw_candidates:

                if self.stats.valid >= target:
                    break

                if raw.post_id in self._seen:
                    continue

                self._seen.add(raw.post_id)
                self.stats.observed += 1
                progressed = True

                try:
                    candidate = self.extractor.extract(raw)

                    # Validation lives inside DatasetWriter's contract
                    # after extraction.
                    from .validator import CandidateValidator

                    result = CandidateValidator().validate(candidate)

                    if result.status == CandidateStatus.VALID:
                        self.writer.store(candidate)
                        self.stats.valid += 1
                    else:
                        self.writer.reject(
                            candidate,
                            result.reason or "unknown",
                        )
                        self.stats.rejected += 1

                except Exception as error:
                    self.stats.errors += 1

                    # We don't let one malformed post kill the run.
                    print(
                        f"[COLLECTOR] candidate error: {error}"
                    )

            if not progressed:
                self.source.next()

        return self.stats