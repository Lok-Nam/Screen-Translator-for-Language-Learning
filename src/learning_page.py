import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout

from card_manager import CardManager

class LearningPage(QWidget):
    def __init__(self):
        super().__init__()
        self.card_manager = CardManager()
        self.current_card_info = None
        self.setupUI()
        self.setMaximumWidth(1000)

    def setupUI(self):
        # main layout for the learning page
        self.layout = QVBoxLayout(self)

        # label to display the number of cards due today
        self.cards_due_label = QLabel()
        self.layout.addWidget(self.cards_due_label)
        self.update_due()

        # button to start the learning session
        self.start_learning_button = QPushButton("Start Learning")
        self.start_learning_button.clicked.connect(self.start_review_session)
        self.layout.addWidget(self.start_learning_button)

        # label and button for card review
        self.review_word_label = QLabel()
        self.layout.addWidget(self.review_word_label)
        self.review_word_label.hide()

        self.reveal_button = QPushButton("Reveal Meaning")
        self.reveal_button.clicked.connect(self.reveal_meaning)
        self.layout.addWidget(self.reveal_button)
        self.reveal_button.hide()

        self.meaning_label = QLabel()
        self.layout.addWidget(self.meaning_label)
        self.meaning_label.hide()

        # feedback buttons
        self.user_feedback_buttons_layout = QHBoxLayout()
        self.again_button = QPushButton()
        self.hard_button = QPushButton()
        self.good_button = QPushButton()
        self.easy_button = QPushButton()
        self.user_feedback_buttons_layout.addWidget(self.again_button)
        self.user_feedback_buttons_layout.addWidget(self.hard_button)
        self.user_feedback_buttons_layout.addWidget(self.good_button)
        self.user_feedback_buttons_layout.addWidget(self.easy_button)
        self.layout.addLayout(self.user_feedback_buttons_layout)

        # hide all feedback buttons initially
        self.again_button.hide()
        self.hard_button.hide()
        self.good_button.hide()
        self.easy_button.hide()

        if self.is_need_learning() == False:
            self.cards_due_label.setText("No cards due for now, good job!")
            self.start_learning_button.hide()
            self.close_button = QPushButton("Close this window")
            self.close_button.clicked.connect(self.close)
            self.layout.addWidget(self.close_button)

    def start_review_session(self):
        self.start_learning_button.hide()
        self.show_next_card()

    def reveal_meaning(self):
        self.reveal_button.hide()
        self.meaning_label.show()
        self.again_button.show()
        self.hard_button.show()
        self.good_button.show()
        self.easy_button.show()

    def handle_feedback(self, feedback_card, time):
        self.meaning_label.hide()
        self.again_button.hide()
        self.hard_button.hide()
        self.good_button.hide()
        self.easy_button.hide()
        self.again_button.disconnect()
        self.hard_button.disconnect()
        self.good_button.disconnect()
        self.easy_button.disconnect()
        self.current_card_info[0][0] = feedback_card
        self.card_manager.update_card_db(self.current_card_info[0])
        self.update_due()
        if self.card_manager.is_complete == True:
            self.end_review_session()
        else:
            self.show_next_card()

    def end_review_session(self):
        self.review_word_label.setText("Review session complete!")

    def show_next_card(self):
        self.current_card_info = self.card_manager.get_card_from_deck()
        card_word = self.current_card_info[0][3]
        card_meaning = self.current_card_info[0][5]
        card_pos = self.current_card_info[0][4]
        card_again = self.current_card_info[1][0]
        card_hard = self.current_card_info[1][1]
        card_good = self.current_card_info[1][2]
        card_easy = self.current_card_info[1][3]

        self.review_word_label.setText(card_word)
        self.review_word_label.show()
        self.reveal_button.show()
        self.meaning_label.setText(f"Meaning: {card_meaning}, POS: {card_pos}")

        time_again = self.card_manager.get_schedule_time(card_again)
        time_hard = self.card_manager.get_schedule_time(card_hard)
        time_good = self.card_manager.get_schedule_time(card_good)
        time_easy = self.card_manager.get_schedule_time(card_easy)
        self.again_button.setText(f"Again ({time_again})")
        self.hard_button.setText(f"Hard ({time_hard})")
        self.good_button.setText(f"Good ({time_good})")
        self.easy_button.setText(f"Easy ({time_easy})")

        self.again_button.clicked.connect(lambda: self.handle_feedback(card_again, time_again))
        self.hard_button.clicked.connect(lambda: self.handle_feedback(card_hard, time_hard))
        self.good_button.clicked.connect(lambda: self.handle_feedback(card_good, time_good))
        self.easy_button.clicked.connect(lambda: self.handle_feedback(card_easy, time_easy))

    def update_due(self):
        card_due = self.card_manager.get_num_card_remain()
        self.cards_due_label.setText(f"Cards due today: new:{card_due[0]}, learning: {card_due[1]}")

    def is_need_learning(self):
        card_due = self.card_manager.get_num_card_remain()
        if card_due[0] + card_due[1] == 0:
            return False
        return True