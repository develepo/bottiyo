import re


class CommandRouter:

    def route(self, command: str):
        command = command.strip()

        if not command:
            return {
                "intent": "empty",
                "args": {},
            }

        # --------------------------------------------------
        # Tuneez Chrome / CDP
        # --------------------------------------------------

        if command.lower() in {
            "open chrome",
            "launch chrome",
            "start chrome",
            "open chrome cdp",
            "launch chrome cdp",
            "start chrome cdp",
            "open tuneez chrome",
            "launch tuneez chrome",
            "start tuneez chrome",
        }:
            return {
                "intent": "chrome_cdp",
                "args": {},
            }

        # --------------------------------------------------
        # URLs
        # --------------------------------------------------

        url_match = re.match(
            r"^(?:open|go to|visit)\s+"
            r"(https?://\S+|www\.\S+)$",
            command,
            re.IGNORECASE,
        )

        if url_match:
            return {
                "intent": "open_url",
                "args": {
                    "url": url_match.group(1)
                },
            }

        # --------------------------------------------------
        # Applications / files
        # --------------------------------------------------

        app_match = re.match(
            r"^(?:open|launch|start)\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if app_match:
            target = app_match.group(1).strip()

            if not target.startswith(
                (
                    "http://",
                    "https://",
                    "www.",
                )
            ):
                return {
                    "intent": "open",
                    "args": {
                        "target": target
                    },
                }

        # --------------------------------------------------
        # Current directory
        # --------------------------------------------------

        if command.lower() in {
            "inspect instagram",
            "inspect instagram tab",
            "inspect instagram page",
        }:
            return {
                "intent": "inspect_instagram",
                "args": {},
            }

        
        if command.lower() in {
            "where am i",
            "current directory",
            "pwd",
            "where are we",
        }:
            return {
                "intent": "cwd",
                "args": {},
            }

        # --------------------------------------------------
        # Shell
        # --------------------------------------------------

        shell_match = re.match(
            r"^(?:run|execute|shell)\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if shell_match:
            return {
                "intent": "shell",
                "args": {
                    "command": shell_match.group(1).strip()
                },
            }

        # --------------------------------------------------
        # Unknown
        # --------------------------------------------------

        return {
            "intent": "unknown",
            "args": {
                "command": command
            },
        }