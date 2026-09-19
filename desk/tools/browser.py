"""Dedicated Chrome CDP integration for Bottiyo browser actions."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import Browser, Playwright, sync_playwright


class BrowserTool:
    """Launch and control Bottiyo's isolated Chrome profile through CDP."""

    CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    HOST = "127.0.0.1"
    PORT = 9222
    STARTUP_TIMEOUT_SECONDS = 10

    def __init__(self) -> None:
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None

    @property
    def cdp_url(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"

    @property
    def profile_dir(self) -> Path:
        temp_dir = os.environ.get("TEMP")
        if not temp_dir:
            raise RuntimeError("Windows TEMP directory unavailable.")
        return Path(temp_dir) / "tuneez-chrome"

    def _is_running(self) -> bool:
        try:
            with urlopen(f"{self.cdp_url}/json/version", timeout=0.5) as response:
                return response.status == 200
        except (URLError, OSError):
            return False

    def launch(self) -> str:
        """Start the dedicated CDP Chrome if it is not already available."""
        if self._is_running():
            return "Bottiyo Chrome is ready."
        if not self.CHROME_PATH.is_file():
            raise FileNotFoundError(f"Chrome not found: {self.CHROME_PATH}")

        profile = self.profile_dir
        profile.mkdir(parents=True, exist_ok=True)
        subprocess.Popen(
            [
                str(self.CHROME_PATH),
                f"--remote-debugging-address={self.HOST}",
                f"--remote-debugging-port={self.PORT}",
                f"--user-data-dir={profile}",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )

        deadline = time.monotonic() + self.STARTUP_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            if self._is_running():
                return f"Bottiyo Chrome started on {self.cdp_url}."
            time.sleep(0.1)
        raise RuntimeError("Chrome started but its CDP endpoint did not become available.")

    def connect(self) -> Browser:
        """Connect Playwright to the running dedicated CDP browser."""
        if self.browser is not None:
            try:
                _ = self.browser.contexts
                return self.browser
            except Exception:
                self.browser = None
        if self.playwright is None:
            self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.connect_over_cdp(self.cdp_url)
        return self.browser

    def inspect_instagram(self) -> dict:
        """Inspect the currently open Instagram tab through CDP."""

        self.launch()
        browser = self.connect()

        if not browser.contexts:
            raise RuntimeError("Bottiyo Chrome has no browser context.")

        pages = []

        for context in browser.contexts:
            pages.extend(context.pages)

        instagram_pages = [
            page
            for page in pages
            if "instagram.com" in page.url.lower()
        ]

        if not instagram_pages:
            raise RuntimeError("No Instagram tab found in Bottiyo Chrome.")

        page = instagram_pages[0]
        page.bring_to_front()

        title = page.title()
        url = page.url

        body_text = page.locator("body").inner_text(
            timeout=10_000
        )

        # Keep the first inspection bounded.
        body_text = body_text[:20_000]

        return {
            "url": url,
            "title": title,
            "body_text": body_text,
        }
    def open_url(self, url: str) -> str:
        """Navigate a tab in Bottiyo Chrome, never the system default browser."""
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        self.launch()
        browser = self.connect()
        if not browser.contexts:
            raise RuntimeError("Bottiyo Chrome has no browser context.")
        context = browser.contexts[0]
        page = context.pages[-1] if context.pages else context.new_page()
        page.bring_to_front()
        page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        return f"Opened {url} in Bottiyo Chrome."

    def close(self) -> None:
        """Disconnect Playwright without closing the persistent Chrome instance."""
        self.browser = None
        if self.playwright is not None:
            try:
                self.playwright.stop()
            finally:
                self.playwright = None


    