from fsrs import *
from database import Database
import datetime
from dateutil.relativedelta import relativedelta
import pickle
import configparser
Config = configparser.ConfigParser()
import random

class CardManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CardManager, cls).__new__(cls)
            cls._instance.initialize()
            return cls._instance
    
    def initialize(self):
        self.db = Database()
        self.f = FSRS()
        self.num_new = 0
        self.num_learning = 0
        self.deck = self.get_today_deck()
        self.is_complete = False

    def get_today_deck(self):
        Config.read('src\config.ini')
        num_new = int(Config.get('daily_limit', 'new'))
        num_review = int(Config.get('daily_limit', 'review'))
        # get current date
        current_date = datetime.datetime.now().date()
        self.db.openConnection()
        # get new state cards first 
        query = f"""
        SELECT flashcard.card, flashcard.id, flashcard.state, vocabulary.word, vocabulary.part_of_speech, vocabulary.meaning
        FROM flashcard
        JOIN vocabulary ON flashcard.vocabularyId = vocabulary.id
        WHERE flashcard.state = 'new' LIMIT {num_new};
        """
        new_card = list(self.db.fetch_data_custom_query(query))
        # get review state cards
        query = f"""
        SELECT flashcard.card, flashcard.id, flashcard.state, vocabulary.word, vocabulary.part_of_speech, vocabulary.meaning
        FROM flashcard
        JOIN vocabulary ON flashcard.vocabularyId = vocabulary.id
        WHERE flashcard.state = 'learning' AND flashcard.next_review <= '{current_date}' LIMIT {num_review};
        """
        review_card = list(self.db.fetch_data_custom_query(query))
        self.db.closeConnection()
        self.num_new = len(new_card)
        self.num_learning = len(review_card)
        deck = new_card + review_card
        for i in range(len(deck)):
            c = list(deck[i])  # convert the tuple from the deck to a list
            c[0] = pickle.loads(c[0])  # deserialize the card
            deck[i] = c  # reassign to the deck as a list

        random.shuffle(deck)  # shuffle the deck
        return deck

    def get_card_from_deck(self):
        # get a card
        if self.deck:
            card = self.deck.pop(0)
        else:
            return None
        card_object = card[0]
        now = datetime.datetime.now()
        # get schedule time according to difficulty in recalling
        scheduling_cards = self.f.repeat(card_object, now)
        card_again = scheduling_cards[Rating.Again].card
        card_hard = scheduling_cards[Rating.Hard].card
        card_good = scheduling_cards[Rating.Good].card
        card_easy = scheduling_cards[Rating.Easy].card
        
        return (card, [card_again, card_hard, card_good, card_easy])
    
    def update_card_db(self, card):
        due_date = card[0].due.date()
        today_date = datetime.date.today()
        if due_date > today_date:
            # card has done reviewing
            # update num cards
            if(card[2] == 'new'):
                self.num_new -= 1
            else:
                self.num_learning -= 1
            self.db.openConnection()
            table = 'flashcard'
            data = {
                'next_review': due_date,
                'state': 'learning',
                'card': pickle.dumps(card[0])
            }
            condition = f"id = {card[1]}"
            self.db.update_data(table, data, condition)
            self.db.closeConnection()
            if(self.num_learning == 0 and self.num_new == 0):
                self.is_complete = True
        else:
            # card has not done reviewing, need to put it back to the deck
            i = 0
            if(card[2] == 'new'):
                self.num_new -= 1
                self.num_learning += 1
                card[2] = 'learning'
            for i in range(len(self.deck)):
                if self.deck[i][0].due < card[0].due:
                    i += 1
                else:
                    self.deck.insert(i, card)
                    return
            # if the card is the last card in the deck
            self.deck.append(card)
        return
    
    def get_num_card_remain(self):
        # get the remaining cards number
        return (self.num_new, self.num_learning)
    
    def get_schedule_time(self, card):
        # get the scheduled time
        now = datetime.datetime.now()
        diff = relativedelta(card.due, now)
        
        if diff.years > 0:
            return f"{diff.years} year" if diff.years == 1 else f"{diff.years} years"
        elif diff.months > 0:
            return f"{diff.months} month" if diff.months == 1 else f"{diff.months} months"
        elif diff.days > 0:
            return f"{diff.days} day" if diff.months == 1 else f"{diff.days} days"
        elif diff.hours > 0:
            return f"{diff.hours} hour" if diff.hours == 1 else f"{diff.hours} hours"
        else:
            return f"{diff.minutes} mins" if diff.minutes >=2 else f"{1} min"