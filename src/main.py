import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from main_worker import MainWorker


from translation_page import TranslationPage
from vocab_page import VocabPage
from grammar_page import GrammarPage
from setting import SettingsPage

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Language Learning Application')
        self.setGeometry(100, 100, 1300, 800)  # set window size

        # create the layout for the sidebar with buttons
        self.sidebar_layout = QVBoxLayout()
        
        # create buttons for the sidebar
        self.btn_translation = QPushButton('Translation')
        self.btn_vocabulary = QPushButton('Vocabulary')
        self.btn_grammar = QPushButton('Grammar')
        self.btn_setting = QPushButton('Setting')
        
        # add buttons to the sidebar layout
        self.sidebar_layout.addWidget(self.btn_translation)
        self.sidebar_layout.addWidget(self.btn_vocabulary)
        self.sidebar_layout.addWidget(self.btn_grammar)
        self.sidebar_layout.addWidget(self.btn_setting)
        
        # create a widget to hold the sidebar layout
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)

        # create the main content area
        self.main_content = QWidget()

        # create the main layout for the window
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar_widget, 1) 
        self.main_layout.addWidget(self.main_content, 4)

        # set the main layout to the center
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.initUI()


    def initUI(self):
        # button connections
        self.btn_translation.clicked.connect(lambda: self.load_page('translation'))
        self.btn_vocabulary.clicked.connect(lambda: self.load_page('vocabulary'))
        self.btn_grammar.clicked.connect(lambda: self.load_page('grammar'))
        self.btn_setting.clicked.connect(lambda: self.load_page('setting'))
    
    def load_page(self, page_type):
        # create and start a worker thread to signal which page to load
        self.worker = MainWorker(page_type)
        self.worker.finished.connect(self.handle_page_request)
        self.worker.start()

    def handle_page_request(self, page_type):
        # create the page in the main thread based on the signal
        if page_type == 'translation':
            page = TranslationPage()
        elif page_type == 'vocabulary':
            page = VocabPage()
        elif page_type == 'grammar':
            page = GrammarPage()
        elif page_type == 'setting':
            page = SettingsPage()
        self.display_page(page)

    def display_page(self, page):
        # clear and update layout with the new page
        current_layout = self.main_content.layout()
        if current_layout:
            # delete old widgets
            while current_layout.count():
                widget_to_remove = current_layout.takeAt(0).widget()
                if widget_to_remove:
                    widget_to_remove.setParent(None)
                    widget_to_remove.deleteLater()
        else:
            self.main_content.setLayout(QVBoxLayout())

        self.main_content.layout().addWidget(page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())