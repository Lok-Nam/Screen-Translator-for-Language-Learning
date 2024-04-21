# vocab_page.py file

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton,
                             QLineEdit, QComboBox, QTableWidgetItem)
from vocab_manager import VocabManager
from editing_vocab import EditVocabPage
from learning_page import LearningPage

class VocabPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.search_vocab()  # uncomment this if you want to search for vocab when the page is opened

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # vocabulary list table
        self.vocab_table = QTableWidget()
        self.vocab_table.setColumnCount(5)
        self.vocab_table.setHorizontalHeaderLabels(['ID', 'Vocab Word', 'Part of Speech', 'Frequency', 'Date Added'])
        self.vocab_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.vocab_table.setSelectionMode(QTableWidget.SingleSelection)
        self.vocab_table.doubleClicked.connect(self.edit_vocab)

        # sidebar layout for controls
        sidebar_layout = QVBoxLayout()

        self.learn_button = QPushButton("Learn")
        self.learn_button.clicked.connect(self.learn_flashcard)

        # textbox for searching
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to search")

        # choosing part of speech
        self.pos_selector = QComboBox()
        self.pos_selector.addItems(["ALL", "ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "SCONJ", "VERB"])  # Add more as needed

        # choosing sorting
        self.sort_selector = QComboBox()
        self.sort_selector.addItems(["ID", "Frequency", "Latest"])

        # search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_vocab)

        # arrange sidebar widgets in the layout
        sidebar_layout.addWidget(self.learn_button)
        sidebar_layout.addWidget(self.search_input)
        sidebar_layout.addWidget(self.pos_selector)
        sidebar_layout.addWidget(self.sort_selector)
        sidebar_layout.addWidget(self.search_button)

        # set the layouts
        main_layout.addWidget(self.vocab_table, 4) 
        main_layout.addLayout(sidebar_layout, 1) 

    def edit_vocab(self):
        selected_row = self.vocab_table.currentRow()
        vocab_id = self.vocab_table.item(selected_row, 0).text()
        edit_dialog = EditVocabPage(vocab_id)
        edit_dialog.exec_()
        return
    

    def search_vocab(self):
        self.vocab_table.setRowCount(0) # clear table
        searched_list = VocabManager().get_vocab_list(self.search_input.text(), self.pos_selector.currentText(), self.sort_selector.currentText())
        for row_number, row_data in enumerate(searched_list):
            self.vocab_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.vocab_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        return
    
    def learn_flashcard(self):
        self.learning_page = LearningPage()
        self.learning_page.show()
        return