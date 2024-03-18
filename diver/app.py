from diver import Diver
import json


def lambda_handler(event, context):
    fail = False
    reason = ""
    body = event.get('body', {})
    if body:
        # The body might be a stringified JSON, so we need to parse it
        params = json.loads(body)
        print(params)
        if 'studentName' in params:
            student_name = params['studentName']
        else:
            reason = reason + "No Student Name provided\n"
            fail = True
        if 'studentEmail' in params:
            student_email = params['studentEmail']
        else:
            reason = reason + "No Student Email provided\n"
            fail = True
        if 'subject' in params:
            subject = params['subject']
        else:
            reason = reason + "No Subject provided\n"
            fail = True
        if 'startDate' in params:
            start_date = params['startDate']
        else:
            reason = reason + "No startDate provided\n"
            fail = True
        if 'endDate' in params:
            end_date = params['endDate']
        else:
            reason = reason + "No endDate provided\n"
            fail = True
        if 'question' in params:
            question = params['question']
        else:
            reason = reason + "No question provided\n"
            fail = True

        if not fail:
            diver = Diver()
            diver.define_parameters(student_name, student_email, start_date, end_date, subject, question)
            result = diver.process_with_openai()

            response = {
                "statusCode": 200,
                "body": json.dumps(result)
            }
            return response
        else:
            response = {
                "statusCode": 401,
                "body": reason
            }
            return response
    else:
        response = {
            "statusCode": 401,
            "body": "Empty Body"
        }
        return response
