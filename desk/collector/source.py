from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from playwright.sync_api import Browser, Page


@dataclass(slots=True)
class RawCandidate:
    post_id: str
    source_url: str
    image_url: str | None
    raw_metadata: dict


class BrowserSource:
    """
    Reads candidate posts from the currently controlled browser page.

    Site-specific extraction should be implemented by subclasses.
    """

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    def current_page(self) -> Page:
        if not self.browser.contexts:
            raise RuntimeError("No browser context available.")

        context = self.browser.contexts[0]

        if not context.pages:
            raise RuntimeError("No browser page available.")

        return context.pages[-1]

    def observe(self) -> list[RawCandidate]:
        """
        Inspect the current page and return candidate posts.

        This base implementation deliberately does not assume
        a particular website.
        """
        page = self.current_page()

        return self.extract_candidates(page)

    def extract_candidates(
        self,
        page: Page,
    ) -> list[RawCandidate]:
        raise NotImplementedError(
            "A source adapter must implement extract_candidates()."
        )

    def next(self) -> None:
        """
        Advance to the next candidate/page.

        Site-specific adapters can override this.
        """
        page = self.current_page()
        page.keyboard.press("PageDown")