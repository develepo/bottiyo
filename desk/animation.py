from PySide6.QtCore import QObject, QTimer, Signal


class AnimationController(QObject):
    frame_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.states = {}
        self.current_state = None
        self.current_frame = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_frame)

    def add_state(self, name, frames, interval=500, loop=True):
        self.states[name] = {
            "frames": frames,
            "interval": interval,
            "loop": loop,
        }

    def set_state(self, name):

        if name not in self.states:
            raise ValueError(f"Unknown animation state: {name}")

        self.current_state = name
        self.current_frame = 0

        config = self.states[name]

        self.timer.stop()

        self.timer.start(config["interval"])

        self._emit_current_frame()

    def _next_frame(self):

        if self.current_state is None:
            return

        config = self.states[self.current_state]
        frames = config["frames"]

        if self.current_frame + 1 >= len(frames):

            if config["loop"]:
                self.current_frame = 0
            else:
                self.timer.stop()
                return

        else:
            self.current_frame += 1

        self._emit_current_frame()

    def _emit_current_frame(self):

        config = self.states[self.current_state]

        frame = config["frames"][self.current_frame]

        self.frame_changed.emit(frame)