import spacy
import xml.etree.ElementTree as ET
from database import Database
import pickle
from fsrs import *
from datetime import datetime

class VocabManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VocabManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self._nlp = None
        self._dict = None
        self.db = Database()

    @property
    def nlp(self):
        if not self._nlp:
            self._nlp = spacy.load("ja_core_news_sm")
        return self._nlp

    @property
    def dict(self):
        if not self._dict:
            self._dict = self.load_jmdict('JMdict_e.xml')
        return self._dict

    def tokenize_and_return_list(self, text):
        doc = self.nlp(text)
        return [(token.text, token.pos_, self.get_meaning(token.text)) for token in doc]
    
    def get_meaning(self, vocab):
        if vocab in self.dict:
            # join all meanings into one string separated by slashes
            return ' / '.join(self.dict[vocab])
        else:
            return "no meaning"
            
    def load_jmdict(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        dictionary = {}
        for entry in root.findall('entry'):
            # get elements
            kanji_elements = entry.findall('k_ele')
            for kanji_element in kanji_elements:
                kanji = kanji_element.find('keb').text
                meanings = self.extract_meanings(entry)
                dictionary[kanji] = meanings
            reading_elements = entry.findall('r_ele')
            for reading_element in reading_elements:
                reading = reading_element.find('reb').text
                meanings = self.extract_meanings(entry)
                dictionary[reading] = meanings

        return dictionary

    def extract_meanings(self, entry):
        senses = entry.findall('sense')
        meanings = [sense.find('gloss').text for sense in senses if sense.find('gloss') is not None]
        return meanings

    
    def store_vocab(self, sentence):
        self.db.openConnection()
        vocab_list = self.tokenize_and_return_list(sentence)
        for word, pos, meaning in vocab_list:
            print(meaning)
            existing_word = self.db.fetch_data('vocabulary', ['id', 'frequency'], f"word='{word}'")
            if existing_word:
                word_id, frequency = existing_word[0]
                self.db.update_data('vocabulary', {'frequency': frequency + 1}, f"id={word_id}")
            else:
                self.db.insert_data('vocabulary', ['word', 'part_of_speech', 'meaning', 'frequency'], (word, pos, meaning, 1))
                this_id = self.db.get_id()
                card = Card()
                serialized = pickle.dumps(card)
                self.db.insert_data('flashcard' , ['next_review', 'state', 'card', 'vocabularyId'], (datetime.now(), 'new', serialized, this_id))
        self.db.closeConnection()

    def get_vocab_list(self, key=None, pos=None, sort_by=None):
        limit = 50  # max length of the return list
        result_list = []
        self.db.openConnection()

        columns = ['id', 'word', 'part_of_speech', 'frequency', 'date_added']
        conditions = []

        if key:
            conditions.append(f"word LIKE '%{key}%'")
        if pos != "ALL":
            conditions.append(f"part_of_speech = '{pos}'")
        
        condition = ' AND '.join(conditions) if conditions else None

        # determine the sorting method based on sort_by
        if sort_by == "ID":
            order_clause = 'ORDER BY id'
        elif sort_by == "Frequency":
            order_clause = 'ORDER BY frequency DESC'
        elif sort_by == "Latest":
            order_clause = 'ORDER BY date_added DESC'

        if condition:
            query = f"SELECT {', '.join(columns)} FROM vocabulary WHERE {condition} {order_clause} LIMIT {limit};"
        else:
            query = f"SELECT {', '.join(columns)} FROM vocabulary {order_clause} LIMIT {limit};"

        result_list = self.db.fetch_data_custom_query(query)

        self.db.closeConnection() 
        return result_list
    
    def get_vocab_by_id(self, vocab_id):
            self.db.openConnection()

            # fetch data from the 'vocabulary' table where the ID matches the specified vocab_id
            columns = ['id', 'word', 'part_of_speech', 'meaning', 'frequency', 'date_added']
            condition = f"id = {vocab_id}"
            vocab_data = self.db.fetch_data('vocabulary', columns, condition)

            self.db.closeConnection()

            if vocab_data:
                # if data is found, return it as a dictionary
                result = {
                    'id': vocab_data[0][0],
                    'word': vocab_data[0][1],
                    'part_of_speech': vocab_data[0][2],
                    'meaning': vocab_data[0][3],
                    'frequency': vocab_data[0][4],
                    'date_added': vocab_data[0][5]
                }
                return result
            else:
                # return None or an empty dictionary if no data was found
                return None


        
    def update_vocab(self, vocab_id, word, part_of_speech, meaning):
        self.db.openConnection()

        # prepare the data for updating
        data = {
            'word': word,
            'part_of_speech': part_of_speech,
            'meaning': meaning
        }

        # condition string
        condition = f"id = {vocab_id}"

        update_result = self.db.update_data('vocabulary', data, condition)

        self.db.closeConnection()  # Close the database connection

        return update_result