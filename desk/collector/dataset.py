from __future__ import annotations

import csv
import json
from pathlib import Path
from threading import Lock

from .models import SongCandidate


class DatasetWriter:
    COLUMNS = (
        "id",
        "post_id",
        "song_id",
        "image_path",
        "song_title",
        "artist",
        "language",
        "why",
    )

    def __init__(self, root: str | Path = "data/tuneez") -> None:
        self.root = Path(root)
        self.images_dir = self.root / "images"
        self.metadata_dir = self.root / "metadata"

        self.dataset_path = self.root / "dataset.csv"
        self.rejections_path = self.root / "rejections.jsonl"

        self._lock = Lock()

        self.root.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        self._ensure_dataset()

    def _ensure_dataset(self) -> None:
        if self.dataset_path.exists():
            return

        with self.dataset_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=self.COLUMNS)
            writer.writeheader()

    def store(self, candidate: SongCandidate) -> str:
        if not candidate.image_path:
            raise ValueError("Cannot store candidate without image_path.")

        if not candidate.song_title:
            raise ValueError("Cannot store candidate without song_title.")

        if not candidate.artist:
            raise ValueError("Cannot store candidate without artist.")

        row_id = candidate.song_id or candidate.post_id

        row = {
            "id": row_id,
            "post_id": candidate.post_id,
            "song_id": candidate.song_id or "",
            "image_path": candidate.image_path,
            "song_title": candidate.song_title,
            "artist": candidate.artist,
            "language": candidate.language or "",
            "why": candidate.why or "",
        }

        with self._lock:
            with self.dataset_path.open(
                "a",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.COLUMNS,
                )
                writer.writerow(row)

            metadata_path = (
                self.metadata_dir / f"{row_id}.json"
            )

            metadata_path.write_text(
                json.dumps(
                    {
                        "post_id": candidate.post_id,
                        "source_url": candidate.source_url,
                        "song_id": candidate.song_id,
                        "song_title": candidate.song_title,
                        "artist": candidate.artist,
                        "language": candidate.language,
                        "image_url": candidate.image_url,
                        "image_path": candidate.image_path,
                        "why": candidate.why,
                        "raw_metadata": candidate.raw_metadata,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

        return row_id

    def reject(
        self,
        candidate: SongCandidate,
        reason: str,
    ) -> None:
        record = {
            "post_id": candidate.post_id,
            "source_url": candidate.source_url,
            "reason": reason,
            "song_id": candidate.song_id,
            "song_title": candidate.song_title,
            "artist": candidate.artist,
            "image_url": candidate.image_url,
            "raw_metadata": candidate.raw_metadata,
        }

        with self._lock:
            with self.rejections_path.open(
                "a",
                encoding="utf-8",
            ) as file:
                file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )