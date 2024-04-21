from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QDialog
from vocab_manager import VocabManager

class EditVocabPage(QDialog):
    def __init__(self, vocab_id, parent=None):
        super().__init__(parent)
        self.vocab_id = vocab_id
        self.info = VocabManager().get_vocab_by_id(self.vocab_id)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Edit Vocabulary')
        self.setGeometry(100, 100, 400, 200) 

        # main layout for editing vocabulary
        layout = QVBoxLayout(self)

        # vocabulary id
        self.id_label = QLabel(f"ID: {self.vocab_id}")
        layout.addWidget(self.id_label)

        # input for the word
        self.word_input = QLineEdit(self.info['word'])
        layout.addWidget(self.word_input)

        # input for the meaning
        self.meaning_input = QLineEdit(self.info['meaning'])
        layout.addWidget(self.meaning_input)

        # comboBox for selecting the part of speech
        self.pos_selector = QComboBox()
        self.pos_selector.addItems(["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "SCONJ", "VERB"])  # Add more options as needed
        self.pos_selector.setCurrentText(self.info['part_of_speech'])  # Set to current part of speech
        layout.addWidget(self.pos_selector)

        self.frequency_label = QLabel(f"ID: {self.info['frequency']}")
        layout.addWidget(self.frequency_label)

        self.date_label = QLabel(f"ID: {self.info['date_added']}")
        layout.addWidget(self.date_label)


        # save and cancel button
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_vocab)
        buttons_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject) 
        buttons_layout.addWidget(self.cancel_button)

        # add buttons layout to the main layout
        layout.addLayout(buttons_layout)

    def save_vocab(self):
        updated_word = self.word_input.text()
        updated_pos = self.pos_selector.currentText()
        updated_meaning = self.meaning_input.text()
        # manage database to save it
        VocabManager().update_vocab(self.vocab_id, updated_word, updated_pos, updated_meaning)
        self.accept()