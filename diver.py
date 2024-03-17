import json

import requests
from openai import OpenAI

progressing_optimal_prompt = \
    ("# context #"
     "you are reviewer for the values of the student's progress based on "
     "the given json parameters."
     "the json consist of summary"
     "on the summary contain the total number of mastered lesson, the Levels Mastered vs target, and accuracy"
     "the lesson mastered is the total number of mastered lesson"
     "the lesson targeted is the total number of target lessons to be mastered"
     "the levels mastered vs is the percentage of the mastered lesson vs the targeted lesson and it is denoted as "
     "fraction value of the percentage, "
     "for example the mastered lessons of 7 and the levels mastered vs  of "
     "0.7 means the target is 10 and this didn't reached the target and the other way around"
     "a mastered lesson of 15 and the level mastered vs of 1.5 means the target is 10 and this reached the "
     "target properly"
     "the accuracy also denoted as a fraction number"
     "#######"
     "# objective #"
     "conclude whether the student are progressing optimally or suboptimally"
     "Suboptimal progress is indicated by mastering less than 70% of the lesson target in the period. Struggling "
     "students often have low accuracy (below 80%)."
     "#######"
     "# style #"
     "the returned result should have reasoning for the decision"
     "######"
     "# tone #"
     "Maintain a professional and positive tone for the student"
     "######"
     "# audience #"
     "Student's guide and counselor"
     "######"
     "# response #"
     "The response should be in the form of JSON with the a yes/no decision, decision description and reasoning in "
     "different element")


class Diver:

    def __init__(self):
        self.academic_data = {}

    def define_parameters(self, name, email, date_start, date_end, subject):
        self.name = name
        self.email = email
        self.date_start = date_start
        self.date_end = date_end
        self.subject = subject

    def download_academic_data(self):
        print("Downloading academic data...")

    def get_coaching_data(self):
        print(f"Downloading coaching data...")

    def find_element(self, data, element):
        found_item = {element: value for key, value in data.items() if element.lower() in key.lower()}

        return found_item

    def process_with_openai(self):
        print("Processing")

        coaching_data = json.load(
            open("sample/Branson Pfiester.language.20240101-20240129.coaching.json", "r", encoding="utf8"))
        academic_data = json.load(
            open("sample/Branson Pfiester.language.20240101-20240129.academic.json", "r", encoding="utf8"))

        progressing_source = self.find_element(academic_data, "Lessons_mastered_and")
        # let's add helper definition of Target  lesson
        for element in progressing_source["Lessons_mastered_and"]:
            target = element["Levels Mastered vs"]
            element["Lessons Targeted"] = int(int(element["Lessons Mastered"])/float(target[" Target"]))
        learning_metrics = self.find_element(academic_data, "Learning_Metrics_per")
        progressing_data = {"summary": progressing_source, "details":learning_metrics}
        print(progressing_data)

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": progressing_optimal_prompt},
                {"role": "user", "content": json.dumps(progressing_source)}
            ]
        )
        print(completion.choices[0].message)


if __name__ == '__main__':
    diver = Diver()
    diver.process_with_openai()
