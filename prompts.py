generic_response = \
  ("# response #"
   "The response should be in the form of JSON format with an element of "
   "decision : a yes/no decision, "
   "decision_description : decision description "
   "reason: the reasoning for the decision made "
   "evidence: the evidence that was used as based for decision"
   "#######")

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
     ""+generic_response
     )

right_level_prompt = \
    ("# context #"
     "you are reviewer whether the student are placed in the right bracket "
     "based on the given json parameters."
     "The provided data are bracketing status and standardized test result and performance"
     "the bracketing status consist of Lower Bound and Upper Bound field which indicates "
     "where the student is currently bracketed"
     "######"
     "# objective #"
     "conclude whether the student is working on the right level"
     "Students should be bracketed by two standardized tests - "
     "one mastered (90%+ score) "
     "and one not yet (score below 90%) in the grade immediately above the mastered one."
     "######"
     "# style #"
     "the returned result should have reasoning for the decision"
     "######"
     "# tone #"
     "Maintain a professional and positive tone for the student"
     "######"
     "# audience #"
     "Student's guide and counselor"
     "######"
     "" + generic_response
     )
