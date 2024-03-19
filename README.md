# Deep Diver

This is a student deep diver application
## AWS deployment (timing out on download phase)
Currently, it is deployed in https://go63ledyl6.execute-api.us-east-1.amazonaws.com/Prod/getRecommendation/ (though at this time of writing it gets timed out on fetching academic data)
The call is a POST call with body as follows
```
  {
    "studentName":"Branson Pfiester",
    "studentEmail": "branson.pfiester@alpha.school",
    "subject":"reading",
    "startDate":"2024-01-01",
    "endDate":"2024-01-29",
    "question":"Is the student struggling? Is there underlying friction or learning strategies that may assist her productivity as part of this new plan?"
  }
```
## Local Run

To run the program you need to
- have python3 and also pip in your system
And follow these steps
- Open terminal in the root directory of the project
- cd diver
- enter the parameter in *input.json* file
- run dive.bat

This would generate a virtual environment and install the necessary modules, and then run the process 

## Code call example 
To call the class in the code would require to instantiate the Dive class
```
diver = Diver()
```
And define the parameter of the student
```
diver.define_parameters('Branson Pfiester', 'branson.pfiester@alpha.school',
                        '2024-01-01', '2024-01-29', 'reading',
                        "Is the student struggling? "
                        "Is there underlying friction or learning strategies that may assist her productivity as part of this new plan?")
```
Running locally require Environment Variable 
- OPENAI_API_KEY: Open AI API key
- ACADEMIC_API_KEY: Academic Data API Key
- COACHING_API_KEY: Coaching API key
and to call the process can be done by calling the method
```
- result = diver.process_with_openai()
```
the result would be in the result. 

# History Note
20240318-1648 - updated key
20240319-1939 - make it 