import os
import html
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLEAPI_PATH")

from google.cloud import translate_v2 as translate

class GoogleTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate(self, text, target_language='en'):
        if not text: # empty text
            return ""
        result = self.client.translate(text, target_language=target_language)
        return html.unescape(result['translatedText'])