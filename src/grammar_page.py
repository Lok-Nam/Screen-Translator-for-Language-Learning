from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QComboBox, QShortcut
from grammar_analyser import GrammarAnalyser

class GrammarPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # text display area for grammar analysis results
        self.text_display_area = QTextEdit()
        self.text_display_area.setReadOnly(True)
        self.text_display_area.setPlaceholderText("Grammar analysis results will be displayed here")
        
        # text input area for user to type in text for grammar analysis
        self.text_input_area = QTextEdit()
        self.text_input_area.setPlaceholderText("Enter text for grammar analysis")

        # sidebar layout for the analysis mode selection and submit button
        self.sidebar_layout = QVBoxLayout()
        
        # widget for choosing mode of analysis
        self.mode_of_analysis_combo = QComboBox()
        self.mode_of_analysis_combo.addItem("Part of Speech Analysis")
        self.mode_of_analysis_combo.addItem("Dependency Analysis")
        self.mode_of_analysis_combo.addItem("ChatGPT Analysis")
        
        # submit button for grammar analysis
        self.submit_button = QPushButton("Analyze")
        self.submit_button.clicked.connect(self.analyze_text)

        # add the mode selection and button to the sidebar layout
        self.sidebar_layout.addWidget(self.mode_of_analysis_combo)
        self.sidebar_layout.addStretch() # add space
        self.sidebar_layout.addWidget(self.submit_button)
        
        # set up the main layout
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.text_display_area)
        content_layout.addWidget(self.text_input_area)
        
        # add content and sidebar layouts to the main layout
        main_layout.addLayout(content_layout, 4)
        main_layout.addLayout(self.sidebar_layout, 1)
        
    def analyze_text(self):
        # get the entered text
        input_text = self.text_input_area.toPlainText()
        input_text = input_text.replace(' ', '')
        self.analyser = GrammarAnalyser()
        
        analysis_mode = self.mode_of_analysis_combo.currentText()
        if(analysis_mode == "Part of Speech Analysis"):
            analysis_results = self.analyser.analyse_sentence_pos(input_text)
            result_text = ""
            for sentence in analysis_results:
                sentence_text = " ".join([f"{word}/{pos}" for word, pos in sentence])
                result_text += sentence_text + "\n\n" 
            self.text_display_area.setPlainText(result_text.strip()) 
        elif(analysis_mode == "Dependency Analysis"):
            analysis_results = self.analyser.analyse_sentence_dep(input_text)
            result_text = ""
            for sentence in analysis_results:
                for token_info in sentence:
                    token_format = f"{token_info['text']} ({token_info['dep']}) <-- {token_info['head']} -- Children: {token_info['children']}"
                    result_text += token_format + "\n"
                result_text += "\n"  # separate sentences
            # set the results to the display area
            self.text_display_area.setPlainText(result_text.strip())
        elif(analysis_mode == "ChatGPT Analysis"):
            analysis_results = self.analyser.analyse_sentence_gpt(input_text)
            self.text_display_area.setPlainText(analysis_results.strip())