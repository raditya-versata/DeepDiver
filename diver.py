import requests
from openai import OpenAI

class Diver:

    def __init__(self):
        self.academic_data = {}
    def download_academic_data(self):
        print("Downloading academic data...")

    def get_coaching_data(self):
        print(f"Downloading coaching data...")

    def process_with_openai(self):
        print("Processing")
        client = OpenAI()

        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
          ]
        )

        print(completion.choices[0].message)

if __name__ == '__main__':
    diver = Diver()
    diver.process_with_openai()