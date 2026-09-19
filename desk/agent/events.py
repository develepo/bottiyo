
from PySide6.QtCore import QObject, Signal

from .protocol import AgentEvent


class AgentEventBus(QObject):
    event = Signal(object)

    def emit_event(self, agent_event: AgentEvent) -> None:
        self.event.emit(agent_event)
