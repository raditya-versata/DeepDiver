import requests

class Diver:

    def __init__(self):
        self.academic_data = {}
    def download_academic_data(self):
        print("Downloading academic data...")

    def get_coaching_data(self):
        print(f"Downloading coaching data...")

    def process_with_openai(self):
        print("Processing")

if __name__ == '__main__':
    diver = Diver()
    diver.process_with_openai()