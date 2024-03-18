# Deep Diver

This is a student deep diver application
## AWS deployment (timing out on download phase)
Currently it is deployed in https://go63ledyl6.execute-api.us-east-1.amazonaws.com/Prod/getRecommendation/ (though at this time of writing it get's timed out on fetching academic data)
The call is a POST call with body as follow
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
the core file is located in folder diver, 
in case that it is needed to be run locally we can just open diver.py and change the parameter defined main function call
the parameter can be modified in line 255

```
    diver.define_parameters('Branson Pfiester', 'branson.pfiester@alpha.school',
                            '2024-01-01', '2024-01-29', 'reading',
                            "Is the student struggling? "
                            "Is there underlying friction or learning strategies that may assist her productivity as part of this new plan?")

```
