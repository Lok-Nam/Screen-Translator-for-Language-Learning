from PyQt5.QtCore import QThread, pyqtSignal

class MainWorker(QThread):
    finished = pyqtSignal(str)  # emit the page type

    def __init__(self, page_type):
        super(MainWorker, self).__init__()
        self.page_type = page_type

    def run(self):
        self.finished.emit(self.page_type)
