"""Concrete local actions used by the deterministic local agent."""

import os
import subprocess
from pathlib import Path

from desk.tools.browser import BrowserTool


class ActionExecutor:
    """Executes non-UI actions; browser lifecycle belongs to ``BrowserTool``."""

    def __init__(self, browser: BrowserTool | None = None) -> None:
        self.browser = browser or BrowserTool()

    def open_chrome_cdp(self) -> str:
        return self.browser.launch()

    def open_url(self, url: str) -> str:
        return self.browser.open_url(url)

    def connect_chrome(self):
        """Compatibility entry point for callers that need the CDP browser."""
        self.browser.launch()
        return self.browser.connect()

    def open_target(self, target: str) -> str:
        target = target.strip()
        try:
            os.startfile(target)
            return f"Opened {target}"
        except FileNotFoundError:
            try:
                subprocess.Popen(target, shell=True)
                return f"Started {target}"
            except Exception as error:
                return f"Couldn't open {target}: {error}"
        except Exception as error:
            return f"Couldn't open {target}: {error}"

    def current_directory(self) -> str:
        return str(Path.cwd())

    
    def inspect_instagram(self) -> dict:
        return self.browser.inspect_instagram()

    def run_shell(self, command: str) -> str:
        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            stdout = process.stdout.strip()
            stderr = process.stderr.strip()
            if process.returncode == 0:
                return stdout or "Command completed."
            return f"Command failed (exit {process.returncode}):\n{stderr or stdout}"
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds."
        except Exception as error:
            return f"Command error: {error}"

    def close(self) -> None:
        self.browser.close()
