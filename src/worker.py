from PyQt5.QtCore import QThread, pyqtSignal
import keyboard

class Worker(QThread):
    activated = pyqtSignal()

    def __init__(self, hotkey, parent=None):
        super(Worker, self).__init__(parent)
        self.hotkey = hotkey

    def run(self):
        # register the hotkey and attach the signal to the handler
        keyboard.add_hotkey(self.hotkey, lambda: self.activated.emit())
        # start an infinite loop that keeps the thread alive
        keyboard.wait()

    def stop(self):
        keyboard.unhook_all_hotkeys()