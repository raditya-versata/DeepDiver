import json

import requests
from openai import OpenAI
import prompts


class Diver:

    def __init__(self):
        self.academic_data = {}
        self.client = OpenAI()

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
        found_item = {key: value for key, value in data.items() if element.lower() in key.lower()}
        return found_item

    def get_openai_suggestion(self, system_prompt, user_prompt):
        return self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

    def process_with_openai(self):
        print("Processing")

        coaching_data = json.load(
            open("sample/Branson Pfiester.reading.20240101-20240129.coaching.json", "r", encoding="utf8"))
        academic_data = json.load(
            open("sample/Branson Pfiester.reading.20240101-20240129.academic.json", "r", encoding="utf8"))

        completion = self.check_progressing_optimally(academic_data)
        print(completion.choices[0].message)

        completion = self.check_working_on_right_level(academic_data)
        print(completion.choices[0].message)

        completion = self.check_2hr_learner(academic_data, coaching_data)
        print(completion.choices[0].message)


    def check_progressing_optimally(self, academic_data):
        print("checking progressing optimally")
        progressing_source = self.find_element(academic_data, "Lessons_mastered_and")
        # let's add helper definition of Target  lesson
        element_name = list(progressing_source.keys())[0]
        for element in progressing_source[element_name]:
            target = element["Levels Mastered vs"]
            element["Lessons Targeted"] = int(int(element["Lessons Mastered"]) / float(target[" Target"]))
        learning_metrics = self.find_element(academic_data, "Learning_Metrics_per")
        progressing_data = {"summary": progressing_source, "details": learning_metrics}
        print(progressing_data)
        completion = self.get_openai_suggestion(prompts.progressing_optimal_prompt, json.dumps(progressing_source))
        return completion

    def check_working_on_right_level(self, academic_data):
        print("checking working on right level")
        standardized_tests = self.find_element(academic_data, "Standardized_Test")
        bracketing_list = self.find_element(academic_data, "Bracketing_status")
        # cleaning bracketing_status to only take the given subject
        element_name = list(bracketing_list.keys())[0]
        bracketing_status = {"bracketing_status": []}
        for element in bracketing_list[element_name]:
            if element["Subject"].lower()== self.subject.lower():
                bracketing_status["bracketing_status"].append(element)
        bracketing_data = {"bracketing_status": bracketing_status, "standardized_tests": standardized_tests}
        print(standardized_tests)
        print(bracketing_status)
        completion = self.get_openai_suggestion(prompts.right_level_prompt, json.dumps(bracketing_data))
        return completion

    def check_2hr_learner(self, academic_data, coaching_data):
        print("checking 2hr learner")
        learning_efficiency = self.find_element(academic_data, "Learning_Efficiency")
        learning_metrics_per_week = self.find_element(academic_data, "Learning_Metrics_per")
        time_commitment = self.find_element(academic_data, "Time_Commitment")

        is_2hr_data = {"time_commitment": time_commitment,
                       "learning_metrics_per_week": learning_metrics_per_week,
                       "learning_efficiency": learning_efficiency,
                       "coaching_data": coaching_data}
        print(is_2hr_data)
        completion = self.get_openai_suggestion(prompts.is_2h_learner, json.dumps(is_2hr_data))

        return completion



if __name__ == '__main__':
    diver = Diver()
    diver.define_parameters('Branson Pfiester', 'branson.pfiester@alpha.school', '2024-01-01', '2024-01-29', 'reading')
    diver.process_with_openai()
