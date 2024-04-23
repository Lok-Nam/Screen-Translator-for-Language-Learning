import spacy
from spacy import displacy
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

class GrammarAnalyser:
    def __init__(self):
        # load the Japanese language model
        self.nlp = spacy.load("ja_core_news_sm")

    def analyse_sentence_pos(self, text):
        # process the text using the spaCy NLP pipeline
        doc = self.nlp(text)
        
        # extract the part of speech for each token in each sentence
        analysis_results = []
        for sent in doc.sents:  # loop sentences
            sentence_results = []
            for token in sent:  # loop tokens
                sentence_results.append((token.text, token.pos_))
            analysis_results.append(sentence_results)

        return analysis_results
    
    def analyse_sentence_dep(self, text):
        doc = self.nlp(text)
        
        # extract the labeled dependencies for each token in each sentence
        analysis_results = []
        for sent in doc.sents: 
            sentence_results = []
            for token in sent:
                sentence_results.append({
                    'text': token.text,
                    'dep': token.dep_,
                    'head': token.head.text,
                    'children': [child.text for child in token.children]
                })
            analysis_results.append(sentence_results)

        return analysis_results
    
    def analyse_sentence_vis(self, text):
        doc = self.nlp(text)
        self.options = {
            'distance': 100,
            'compact': True,
            'bg': '#fafafa',
            'color': '#000000',
            'font': 'Arial'
        }
        html = displacy.render(doc, style='dep', page=True, options=self.options)
        return html
    
    def analyse_sentence_gpt(self, text):
        load_dotenv()
        key = os.getenv("gptapi")
        client = OpenAI(
            api_key = key
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": f"Analyze and provide a short grammar structure breakdown, no need translation: \n\n{text}\n"}],
            )
            
            # extract the text from the response
            analysis_result = response.choices[0].message.content.strip()
            return analysis_result
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)