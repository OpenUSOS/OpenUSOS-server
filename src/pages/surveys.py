import os
import json

class Surveys():

    def __init__(self, caller):
        self.caller = caller

    def get_surveys(self):
        surveys = self.caller.api.get('services/surveys/surveys_to_fill2', fields= 'name|id|start_date|end_date|questions')
        json_string = json.dumps(surveys)
        return json_string
    
    def answer_survey(self, my_survey_id, my_anserws):
        try:
            check = self.caller.api.get('services/surveys/fill_out2', survey_id = my_survey_id, answers = my_anserws)
            if check:
                return "N"
            else:
                return "Y"
        except:
            return "N"
