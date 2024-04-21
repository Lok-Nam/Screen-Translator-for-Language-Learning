import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

class gptTranslate:
    def __init__(self):
        return


    def translate(self, text):
        load_dotenv()
        key = os.getenv("gptapi")
        client = OpenAI(
            api_key = key
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": f"Translate this sentence: \n\n{text}\n"}],
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
            
        return