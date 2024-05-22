import os
import json

class Surveys():

    def __init__(self, caller):
        self.caller = caller

    def get_surveys(self):
        surveys = self.caller.api.get('services/surveys/surveys_to_fill2', fields= 'name|id|start_date|end_date|questions[id|number|display_text_html|possible_answers[id|display_text_html]]')
        json_string = json.dumps(surveys)
        return json_string
    
    def anserw_survey(self, my_survey_id, my_anserws):
        try:
            check = self.caller.api.get('services/surveys/fill_out2', survey_id = my_survey_id, answers = my_anserws)
            if check:
                return "The survey wasn't filled in correctly. Try again."
            else:
                return "Survey sucesfully filled out."
        except:
            return "The survey wasn't filled in correctly. Try again."
