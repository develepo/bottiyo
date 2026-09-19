"""Local mediator between Bottiyo's UI and its deterministic tools."""

from __future__ import annotations

from uuid import uuid4

from PySide6.QtCore import QMetaObject, QObject, QThread, Qt, Signal, Slot

from .events import AgentEventBus
from .executor import ActionExecutor
from .protocol import AgentEvent, AgentTask
from .router import CommandRouter


class _AgentWorker(QObject):
    event_ready = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.router = CommandRouter()
        self.executor = ActionExecutor()

    def _emit(self, task: AgentTask, event_type: str, message: str, **data: object) -> None:
        self.event_ready.emit(AgentEvent(task.task_id, event_type, message, data))

    @Slot(object)
    def handle_task(self, task: AgentTask) -> None:
        self._emit(task, "thinking", "Thinking...")
        try:
            route = self.router.route(task.message)
            intent = route["intent"]
            args = route["args"]
            if intent == "empty":
                result = "What should I do?"

            elif intent == "inspect_instagram":
                self._emit(
                    task,
                    "working",
                    "Inspecting Instagram..."
                )

                observation = self.executor.inspect_instagram()

                result = (
                    f"Instagram found.\n"
                    f"URL: {observation['url']}\n"
                    f"Title: {observation['title']}\n\n"
                    f"{observation['body_text']}"
                )
            elif intent == "open_url":
                self._emit(task, "working", "Opening Bottiyo Chrome...")
                result = self.executor.open_url(args["url"])
            elif intent == "open":
                self._emit(task, "working", "Opening...")
                result = self.executor.open_target(args["target"])
            elif intent == "cwd":
                result = self.executor.current_directory()
            elif intent == "shell":
                self._emit(task, "working", "Working...")
                result = self.executor.run_shell(args["command"])
            elif intent == "chrome_cdp":
                self._emit(task, "working", "Starting Bottiyo Chrome...")
                result = self.executor.open_chrome_cdp()
            else:
                result = "I don't know how to do that yet."
            self._emit(task, "completed", str(result), intent=intent)
        except Exception as error:
            self._emit(task, "failed", str(error))

    @Slot()
    def shutdown(self) -> None:
        self.executor.close()


class LocalAgent(QObject):
    """Queues local commands off the UI thread and emits progress events."""

    task_submitted = Signal(object)

    def __init__(self, event_bus: AgentEventBus, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.event_bus = event_bus
        self._thread = QThread(self)
        self._worker = _AgentWorker()
        self._worker.moveToThread(self._thread)
        self.task_submitted.connect(self._worker.handle_task, Qt.QueuedConnection)
        self._worker.event_ready.connect(self.event_bus.emit_event, Qt.QueuedConnection)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.start()

    def submit(self, message: str, metadata: dict[str, object] | None = None) -> str:
        task = AgentTask(uuid4().hex, message, metadata or {})
        self.task_submitted.emit(task)
        return task.task_id

    def close(self) -> None:
        if not self._thread.isRunning():
            return
        QMetaObject.invokeMethod(
            self._worker,
            "shutdown",
            Qt.BlockingQueuedConnection,
        )
        self._thread.quit()
        self._thread.wait(3_000)
