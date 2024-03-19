import json
import os

import requests
from openai import OpenAI
import prompts


class Diver:

    def __init__(self,
                 openai_api_key=os.environ.get("OPENAI_API_KEY"),
                 academic_token=os.environ.get("ACADEMIC_API_KEY"),
                 coaching_token=os.environ.get("COACHING_API_KEY")
                 ):
        self.inquiry = None
        self.subject = None
        self.date_end = None
        self.date_start = None
        self.name = None
        self.email = None
        self.academic_data = {}
        self.client = OpenAI(api_key=openai_api_key)
        self.academic_token = academic_token
        self.coaching_token = coaching_token

    def define_parameters(self, name, email, date_start, date_end, subject, inquiry):
        self.name = name
        self.email = email
        self.date_start = date_start
        self.date_end = date_end
        self.subject = subject
        self.inquiry = inquiry

    def get_academic_data(self):
        print("Downloading academic data...")
        token = self.academic_token
        print(token)
        headers = {
            'Authorization': f"{token}"
        }

        parameters = {
            "student": self.name,
            "subject": self.subject,
            "startDate": self.date_start,
            "endDate": self.date_end
        }
        response = requests.get("https://hpjgmbk65zgzff64b6y7vhw2ua0sytlh.lambda-url.us-east-1.on.aws",
                                params=parameters, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Checking if 'url' is in the JSON response
            if 'url' in data:
                # If 'url' exists, we use it for another GET request
                second_response = requests.get(data['url'])
                if second_response.status_code == 200:
                    # Return the JSON data from the second request
                    return second_response.json()
                else:
                    raise Exception(f"Second request failed with status {second_response.status_code}")
            else:
                raise Exception("'url' not found in the received JSON")
        else:
            raise Exception(f"First request failed with status {response.status_code}")

    def get_coaching_data(self):
        print(f"Downloading coaching data...")
        token = self.coaching_token
        print(token)
        headers = {
            'Authorization': f"{token}"
        }
        parameters = {
            "email": self.email,
            "startDate": self.date_start,
            "endDate": self.date_end,
            "subject": self.subject
        }
        response = requests.get("https://mk62mbxkbe6flyv44eli5shrhi0hinml.lambda-url.us-east-1.on.aws",
                                params=parameters, headers=headers)
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            raise Exception(f"Request failed with status {response.status_code}")

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

        # coaching_data = json.load(
        #     open("sample/Branson Pfiester.reading.20240101-20240129.coaching.json", "r", encoding="utf8"))
        # academic_data = json.load(
        #     open("sample/Branson Pfiester.reading.20240101-20240129.academic.json", "r", encoding="utf8"))
        academic_data = self.get_academic_data()
        coaching_data = self.get_coaching_data()

        progress_completion = self.check_progressing_optimally(academic_data)
        # print(progress_completion.choices[0].message.content)

        level_completion = self.check_working_on_right_level(academic_data)
        # print(level_completion.choices[0].message.content)

        learner_2hr_completion = self.check_2hr_learner(academic_data, coaching_data)
        # print(learner_2hr_completion.choices[0].message.content)

        summary_data = {
            "progressing_optimally": json.loads(progress_completion.choices[0].message.content),
            "correct_level": json.loads(level_completion.choices[0].message.content),
            "2hr_learner": json.loads(learner_2hr_completion.choices[0].message.content)
        }

        reason_progress_completion = self.check_reason_for_lack_of_progression(academic_data, coaching_data,
                                                                               summary_data)
        # print(reason_progress_completion.choices[0].message.content)
        summary_data["reason_progress_completion"] = json.loads(reason_progress_completion.choices[0].message.content)

        other_insight_completion = self.check_other_insight(academic_data, coaching_data, summary_data)
        summary_data["other_insight"] = json.loads(other_insight_completion.choices[0].message.content)

        important_completion = self.answer_important_problem(academic_data, coaching_data, summary_data)
        # print(important_completion.choices[0].message.content)

        summary_data["important_problem"] = json.loads(important_completion.choices[0].message.content)

        need_todo_completion = self.answer_what_need_to_be_done(academic_data, coaching_data, summary_data)

        summary_data["alpha_needs_todo"] = json.loads(need_todo_completion.choices[0].message.content)

        student_suggestion_completion = self.answer_suggestion_for_student(academic_data, coaching_data, summary_data)
        # print(student_suggestion_completion.choices[0].message.content)
        summary_data["student_suggestion"] = json.loads(student_suggestion_completion.choices[0].message.content)

        # print(summary_data)

        return summary_data

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
            if element["Subject"].lower() == self.subject.lower():
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

    def check_reason_for_lack_of_progression(self, academic_data, coaching_data, summary_data):
        print("checking reason for lack of progression")

        progress_data = {
            "summary": summary_data,
            "academic_data": academic_data,
            "coaching_data": coaching_data
        }

        completion = self.get_openai_suggestion(prompts.reason_of_progression, json.dumps(progress_data))
        return completion

    def check_other_insight(self, academic_data, coaching_data, summary_data):
        print("checking other insight")
        important_data = {
            "summary": summary_data,
            "academic_data": academic_data,
            "coaching_data": coaching_data
        }
        completion = self.get_openai_suggestion(prompts.other_insight_prompt(self.inquiry), json.dumps(important_data))
        return completion

    def answer_important_problem(self, academic_data, coaching_data, summary_data):
        print("answering important problem")
        important_data = {
            "summary": summary_data,
            "academic_data": academic_data,
            "coaching_data": coaching_data
        }
        prompt = prompts.important_problem_prompt(json.dumps(important_data),
                                                  "After you perform your analysis, this can be see in summary_data, "
                                                  "summarize your findings in a way that"
                                                  "clearly explains the causes of the problem statement")
        completion = self.get_openai_suggestion(prompt, self.inquiry)
        return completion

    def answer_what_need_to_be_done(self, academic_data, coaching_data, summary_data):
        print("answering what_need_to_be_done")
        important_data = {
            "summary": summary_data,
            "academic_data": academic_data,
            "coaching_data": coaching_data
        }
        prompt = prompts.important_problem_prompt(json.dumps(important_data),
                                                  "Clearly state what needs to be done and by whom to fix the problem "
                                                  "and help the student learn more effectively.")
        completion = self.get_openai_suggestion(prompt, self.inquiry)
        return completion

    def answer_suggestion_for_student(self, academic_data, coaching_data, summary_data):
        print("answering suggestion_for_student")
        important_data = {
            "summary": summary_data,
            "academic_data": academic_data,
            "coaching_data": coaching_data
        }
        prompt = prompts.message_to_student_prompt
        completion = self.get_openai_suggestion(prompt, json.dumps(important_data))
        return completion


if __name__ == '__main__':
    input_json = json.load(open('input.json', encoding='utf8'))
    api_key = input("Please enter the open api key: ")
    academic_key = input("Please enter the Academic API key ")
    coaching_key = input("Please enter the Coaching API key ")
    if (api_key == "") or (academic_key == "") or (coaching_key == ""):
        print("you didn't enter one of the key, defaulting to use Environment Variables\n"
              "Needed environment variables are:\n"
              "- OPENAI_API_KEY: Open AI API key\n"
              "- ACADEMIC_API_KEY: Academic Data API Key\n"
              "- COACHING_API_KEY: Coaching API key")
        diver = Diver()
    else:
        diver = Diver(api_key, academic_key, coaching_key)
    studentName = input_json["studentName"]
    studentEmail = input_json["studentEmail"]
    subject = input_json["subject"]
    startDate = input_json["startDate"]
    endDate = input_json["endDate"]
    question = input_json["question"]
    diver.define_parameters(studentName, studentEmail,
                            startDate, endDate, subject,
                            question)
    result = diver.process_with_openai()
    json.dump(result, open("output.json", "w", encoding="utf8"))
