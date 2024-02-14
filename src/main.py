import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence

from screen_capture import capture_screen
from assign_key import assign_key

import configparser
Config = configparser.ConfigParser()
Config.read('src\config.ini')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 300, 200)  # x, y, width, height

        # Create a central widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create a vertical layout
        self.layout = QVBoxLayout()
        
        # Create buttons and add them to the layout
        self.shortcut = QShortcut(QKeySequence(Config.get('CaptureKey', 'Key')), self)
        self.shortcut.activated.connect(capture_screen)

        self.button2 = QPushButton("assign key for screen capture")
        self.button2.clicked.connect(lambda: assign_key(self.update_shortcut))
        self.layout.addWidget(self.button2)

        self.button3 = QPushButton("Open Page 3")
        self.button3.clicked.connect(self.on_click_button3)
        self.layout.addWidget(self.button3)

        # Set the layout on the central widget
        self.centralWidget.setLayout(self.layout)

    def on_click_button3(self):
        print("Button 3 clicked")

    def update_shortcut(self):
        # Re-read the configuration file to get the updated key
        Config.read('src\config.ini')
        new_key_sequence = QKeySequence(Config.get('CaptureKey', 'Key'))
        # Update the shortcut with the new key sequence
        self.shortcut.setKey(new_key_sequence)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
