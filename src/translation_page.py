from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from screen_capture import capture_screen

import configparser
import ocr
from worker import Worker

from google_translate_api import GoogleTranslator
from vocab_manager import VocabManager

from gpt_api import gptTranslate

import configparser
Config = configparser.ConfigParser()
Config.read('src\config.ini')

class TranslationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_keyboard_listener()
        self.translator = GoogleTranslator()
        self.translatorGPT = gptTranslate()


    def init_ui(self):
        # main layout for the translation page
        layout = QVBoxLayout(self)

        # text area for displaying translated text
        self.translated_text_area = QTextEdit(self)
        self.translated_text_area.setReadOnly(True)  # Make this area read-only
        self.translated_text_area.setPlaceholderText("Translated Text will be displayed here")
        
        # text area for inputting text
        self.input_text_area = QTextEdit(self)
        self.input_text_area.setPlaceholderText("Textbox for entering")

        # button for submitting input text
        self.submit_button = QPushButton("Button to submit")

        # arrange the widgets in the layout
        layout.addWidget(self.translated_text_area)
        layout.addWidget(self.input_text_area)
        layout.addWidget(self.submit_button)

        # set the main layout of the widget
        self.setLayout(layout)

        # connect the submit button to the translation function
        self.submit_button.clicked.connect(self.translate_text)
    
    def init_keyboard_listener(self):
        Config = configparser.ConfigParser()
        Config.read('src\\config.ini')
        hotkey = Config.get('CaptureKey', 'Key')

        self.worker = Worker(hotkey)
        self.worker.activated.connect(self.captured)
        self.worker.start()

    def translate_text(self):
        input_text = self.input_text_area.toPlainText()
        input_text = input_text.replace(' ', '')
        VocabManager().store_vocab(input_text)
        translate_way = Config.get('translation', 'using')
        if translate_way == 'google':
            translated_text = self.translator.translate(input_text)
        else:
            translated_text = self.translatorGPT.translate(input_text)
        self.translated_text_area.setPlainText(f"Translated text for: {input_text} : {translated_text}")

    def captured(self):
        capture_screen()
        imageText = ocr.extract_text_from_image()
        imageText = imageText.replace(' ', '')
        self.input_text_area.setPlainText(f"{imageText}")

    def closeEvent(self, event):
        # clean up the thread when the window is closed
        self.worker.stop()
        self.worker.wait()
        super().closeEvent(event)
