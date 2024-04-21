from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QDialog
from assign_key import assign_key

from PyQt5.QtGui import QKeySequence
import configparser
Config = configparser.ConfigParser()
Config.read('src\config.ini')

class card_limit(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        Config.read('src\config.ini')
        self.ask_user = QLabel("Enter the daily card limit:")
        self.input_new = QLineEdit(f"Daily new card limit:{Config.get('daily_limit', 'new')}")
        self.input_learning = QLineEdit(f"Daily learning card limit:{Config.get('daily_limit', 'review')}")

        layout.addWidget(self.ask_user)
        layout.addWidget(self.input_new)
        layout.addWidget(self.input_learning)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # QDialog built-in method to close the dialog
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)
    
    def save(self):
        Config.read('src\config.ini')
        Config.set('daily_limit', 'new', self.input_new.text())
        Config.set('daily_limit', 'review', self.input_learning.text())
        Config.write(open('src\config.ini', 'w'))
        self.accept()

class translateMethod(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.ask_user = QLabel("Choose which method to translate text")
        self.gpt_button = QPushButton("GPT")
        self.gpt_button.clicked.connect(self.gpt)
        self.google_button = QPushButton("Google")
        self.google_button.clicked.connect(self.google)
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.reject)
        layout.addWidget(self.ask_user)
        layout.addWidget(self.gpt_button)
        layout.addWidget(self.google_button)
        layout.addWidget(self.cancel)
        self.setLayout(layout)


    def gpt(self):
        Config.read('src\config.ini')
        Config.set('translation', 'using', 'gpt')
        Config.write(open('src\config.ini', 'w'))
        self.accept()

    def google(self):
        Config.read('src\config.ini')
        Config.set('translation', 'using', 'google')
        Config.write(open('src\config.ini', 'w'))
        self.accept()




class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.btn_assignKey = QPushButton("Assign Key")
        self.btn_set_daily_card_limit = QPushButton("Set Daily Card Limit")
        self.btn_set_daily_card_limit.clicked.connect(self.set_daily_card_limit)

        layout.addWidget(self.btn_assignKey)
        layout.addWidget(self.btn_set_daily_card_limit)

        self.btn_set_translation = QPushButton("Set Translation Method")
        self.btn_set_translation.clicked.connect(self.set_translation)
        layout.addWidget(self.btn_set_translation)

        self.setLayout(layout)
        self.btn_assignKey.clicked.connect(lambda: assign_key(self.update_shortcut))
        self.daily_card_limit_dialog = None
        self.set_translation_dialog = None


        

    def update_shortcut(self):
        # get the updated key
        Config.read('src\config.ini')
        new_key_sequence = QKeySequence(Config.get('CaptureKey', 'Key'))

    def set_daily_card_limit(self):
        # check if the dialog is already displayed
        if self.daily_card_limit_dialog is None or not self.daily_card_limit_dialog.isVisible():
            self.daily_card_limit_dialog = card_limit()
            self.daily_card_limit_dialog.show()
        else:
            # bring the existing dialog to the front if it is already open
            self.daily_card_limit_dialog.raise_()
            self.daily_card_limit_dialog.activateWindow()

    def set_translation(self):
        if self.set_translation_dialog is None or not self.set_translation_dialog.isVisible():
            self.set_translation_dialog = translateMethod()
            self.set_translation_dialog.show()
        else:
            self.set_translation_dialog.raise_()
            self.set_translation_dialog.activateWindow()