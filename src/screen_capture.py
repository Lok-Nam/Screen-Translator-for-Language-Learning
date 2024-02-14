from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import Qt, QRect

class CropTool(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.cropped_pixmap = None
        self.begin = None
        self.end = None
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(self.original_pixmap.rect())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.original_pixmap)
        if self.begin and self.end:
            rect = QRect(self.begin, self.end)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        self.cropped_pixmap = self.original_pixmap.copy(QRect(self.begin, self.end))
        self.cropped_pixmap.save('cropped_image.png')

def capture_screen():
    app = QApplication.instance()  # Checks if QApplication already exists
    if not app:  # Create a new instance if it does not exist
        app = QApplication([])
    screen = QGuiApplication.primaryScreen()
    screenshot = screen.grabWindow(0)
    crop_tool = CropTool(screenshot)
    crop_tool.exec_()
