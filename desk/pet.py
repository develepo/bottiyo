from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QPoint,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    Property,
    QSize,
)
from PySide6.QtGui import (
    QImage,
    QPainter,
    QPixmap,
)
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
)

from .animation import AnimationController
from .agent.events import AgentEventBus
from .agent.local_agent import LocalAgent
from .agent.protocol import AgentEvent


class PetWindow(QWidget):

    PET_SIZE = 150

    def __init__(self):
        super().__init__()

        # ==================================================
        # WINDOW
        # ==================================================

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setMouseTracking(True)

        self.window_width = self.PET_SIZE + 80
        self.window_height = self.PET_SIZE + 170

        self.resize(
            self.window_width,
            self.window_height,
        )

        # ==================================================
        # DRAGGING
        # ==================================================

        self.drag_position = QPoint()

        # ==================================================
        # ASSETS
        # ==================================================

        self.asset_dir = (
            Path(__file__).resolve().parent
            / "assets"
            / "panda"
        )

        print("[ASSETS]", self.asset_dir)

        # ==================================================
        # AGENT
        # ==================================================

        self.event_bus = AgentEventBus(self)
        self.agent = LocalAgent(self.event_bus, self)
        self.event_bus.event.connect(self._handle_agent_event)

        # ==================================================
        # PANDA
        # ==================================================

        self.character = QLabel(self)

        self.character.setAlignment(
            Qt.AlignCenter
        )

        self.character.setGeometry(
            40,
            10,
            self.PET_SIZE,
            self.PET_SIZE,
        )

        self.character.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.character.setMouseTracking(True)

        # ==================================================
        # FLOAT ANIMATION
        # ==================================================

        self._float_offset = 0

        self.float_animation = QPropertyAnimation(
            self,
            b"float_offset",
            self,
        )

        self.float_animation.setDuration(
            1800
        )

        self.float_animation.setStartValue(
            -4
        )

        self.float_animation.setEndValue(
            4
        )

        self.float_animation.setEasingCurve(
            QEasingCurve.InOutSine
        )

        self.float_animation.setLoopCount(
            -1
        )

        self.float_animation.start()

        # ==================================================
        # STATUS BUBBLE
        # ==================================================

        self.status = QLabel(
            "Hey! 👋",
            self,
        )

        self.status.setAlignment(
            Qt.AlignCenter
        )

        self.status.setWordWrap(True)

        self.status.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(20, 20, 25, 235);
                border-radius: 15px;
                padding: 7px 14px;
                font-size: 13px;
            }
        """)

        self.status.setGeometry(
            20,
            self.PET_SIZE + 20,
            self.PET_SIZE - 40,
            32,
        )

        # ==================================================
        # INPUT
        # ==================================================

        self.input = QLineEdit(self)

        self.input.setPlaceholderText(
            "Tell me what to do..."
        )

        self.input.setGeometry(
            20,
            self.PET_SIZE + 70,
            self.PET_SIZE + 40,
            42,
        )

        self.input.setStyleSheet("""
            QLineEdit {
                background: rgba(20, 20, 25, 240);
                color: white;
                border: 1px solid rgba(255, 255, 255, 45);
                border-radius: 21px;
                padding-left: 16px;
                padding-right: 16px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 100);
            }

            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 120);
            }
        """)

        self.input.returnPressed.connect(
            self.submit_command
        )

        # ==================================================
        # ANIMATION CONTROLLER
        # ==================================================

        self.animation = AnimationController(
            self
        )

        self._register_animations()

        self.animation.frame_changed.connect(
            self._set_frame
        )

        self.animation.set_state(
            "idle"
        )

        # ==================================================
        # BLINK
        # ==================================================

        self.blink_timer = QTimer(
            self
        )

        self.blink_timer.timeout.connect(
            self._blink
        )

        self.blink_timer.start(
            3200
        )

        # ==================================================
        # HOVER
        # ==================================================

        self.hover_timer = QTimer(
            self
        )

        self.hover_timer.setSingleShot(
            True
        )

        self.hover_timer.timeout.connect(
            self._show_hover_state
        )

    # ======================================================
    # FLOAT PROPERTY
    # ======================================================

    def get_float_offset(self):
        return self._float_offset

    def set_float_offset(self, value):

        self._float_offset = value

        if not hasattr(
            self,
            "character",
        ):
            return

        self.character.move(
            40,
            10 + int(value),
        )

    float_offset = Property(
        float,
        get_float_offset,
        set_float_offset,
    )

    # ======================================================
    # ANIMATIONS
    # ======================================================

    def _register_animations(self):

        self.animation.add_state(
            "idle",
            [
                self._asset(
                    "idle.svg"
                )
            ],
            1000,
            loop=True,
        )

        self.animation.add_state(
            "blink",
            [
                self._asset(
                    "idle.svg"
                ),
                self._asset(
                    "blink.svg"
                ),
                self._asset(
                    "idle.svg"
                ),
            ],
            120,
            loop=False,
        )

        self.animation.add_state(
            "thinking",
            [
                self._asset(
                    "thinking.svg"
                )
            ],
            500,
            loop=True,
        )

        self.animation.add_state(
            "working",
            [
                self._asset(
                    "working.svg"
                )
            ],
            180,
            loop=True,
        )

        self.animation.add_state(
            "happy",
            [
                self._asset(
                    "happy.svg"
                )
            ],
            500,
            loop=True,
        )

    # ======================================================
    # ASSET PATH
    # ======================================================

    def _asset(self, filename):

        path = (
            self.asset_dir
            / filename
        )

        if not path.exists():

            print(
                "[ERROR] Missing asset:",
                path,
            )

        return str(path)

    # ======================================================
    # SVG RENDERING
    # ======================================================

    def _set_frame(self, path):

        renderer = QSvgRenderer(
            str(path)
        )

        if not renderer.isValid():

            print(
                "[ERROR] Invalid SVG:",
                path,
            )

            return

        size = QSize(
            self.PET_SIZE,
            self.PET_SIZE,
        )

        image = QImage(
            size,
            QImage.Format_ARGB32,
        )

        image.fill(
            Qt.transparent
        )

        painter = QPainter(
            image
        )

        renderer.render(
            painter
        )

        painter.end()

        self.character.setPixmap(
            QPixmap.fromImage(
                image
            )
        )

    # ======================================================
    # STATE
    # ======================================================

    def set_state(
        self,
        state,
        message=None,
    ):

        self.animation.set_state(
            state
        )

        if message is not None:

            self.status.setText(
                str(message)
            )

    # ======================================================
    # BLINK
    # ======================================================

    def _blink(self):

        if (
            self.animation.current_state
            != "idle"
        ):
            return

        self.animation.set_state(
            "blink"
        )

        QTimer.singleShot(
            400,
            self._return_to_idle,
        )

    def _return_to_idle(self):

        if (
            self.animation.current_state
            == "blink"
        ):

            self.animation.set_state(
                "idle"
            )

    # ======================================================
    # HOVER
    # ======================================================

    def enterEvent(self, event):

        self.hover_timer.start(
            300
        )

        super().enterEvent(
            event
        )

    def leaveEvent(self, event):

        self.hover_timer.stop()

        if self.animation.current_state in (
            "thinking",
            "working",
        ):
            super().leaveEvent(
                event
            )
            return

        self.set_state(
            "idle",
            "I'm here.",
        )

        super().leaveEvent(
            event
        )

    def _show_hover_state(self):

        if (
            self.animation.current_state
            == "idle"
        ):

            self.set_state(
                "happy",
                "Hey! 👋",
            )

    # ======================================================
    # COMMAND INPUT
    # ======================================================

    def submit_command(self):

        command = (
            self.input.text()
            .strip()
        )

        if not command:
            return

        self.input.clear()

        self.handle_command(
            command
        )

    # ======================================================
    # COMMAND ROUTING
    # ======================================================

    def handle_command(
        self,
        command,
    ):
        self._active_task_id = self.agent.submit(command)

    def _handle_agent_event(self, event: AgentEvent):
        """Translate agent lifecycle events into panda UI states."""
        message = str(event.message)
        if len(message) > 180:
            message = message[:177] + "..."

        if event.type == "thinking":
            self.set_state("thinking", message)
        elif event.type == "working":
            self.set_state("working", message)
        elif event.type == "completed":
            self.set_state("happy", message)
            QTimer.singleShot(3000, lambda: self._return_to_ready(event.task_id))
        elif event.type == "failed":
            self.set_state("thinking", message)
            QTimer.singleShot(3500, lambda: self._return_to_ready(event.task_id))

    def _return_to_ready(self, task_id):
        if task_id == getattr(self, "_active_task_id", None):
            self.set_state("idle", "Ready.")

    def closeEvent(self, event):
        self.agent.close()
        super().closeEvent(event)

    # ======================================================
    # MOUSE DRAGGING
    # ======================================================

    def mousePressEvent(
        self,
        event,
    ):

        if (
            event.button()
            == Qt.LeftButton
        ):

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

            return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event,
    ):

        if (
            event.buttons()
            & Qt.LeftButton
        ):

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

            return

        super().mouseMoveEvent(
            event
        )

    # ======================================================
    # DOUBLE CLICK
    # ======================================================

    def mouseDoubleClickEvent(
        self,
        event,
    ):

        if (
            event.button()
            == Qt.LeftButton
        ):

            self.close()

            return

        super().mouseDoubleClickEvent(
            event
        )
