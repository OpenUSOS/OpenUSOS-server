import os
import json

class Grades():

    def __init__(self, caller):
        self.caller = caller

    def get_grades(self):
        lista = []
        ids = self.caller.api.get('services/grades/latest', days = 9999, fields='exam_id|exam_session_number')
        for id in ids:
            all = self.caller.api.get('services/grades/grade', exam_id = id["exam_id"], exam_session_number = id["exam_session_number"],
                                        fields='date_modified|modification_author|value_symbol|grade_type_id|course_edition[course_name|term_id]|unit[id]')
            grade = {}
            grade["date"] = all["date_modified"] #grade date
            grade["author"] = all["modification_author"] #grade author
            grade["value"] = all["value_symbol"] #grade value

            #I need the type of the group:
            unitid = all["unit"]["id"]
            unitstuff = self.caller.api.get('services/courses/unit', unit_id = unitid, fields='groups[class_type_id]')
            grade["class_type"] = unitstuff["groups"][0]["class_type_id"] #doesn't matter which, really (I hope)
            #course to get the name of the course
            course = all["course_edition"]
            names = course["course_name"]

            grade["name"] = names["pl"] #grade course name
            grade["term"] = course["term_id"] #grade term

            lista.append(grade)
        json_string = json.dumps(lista)
        return json_string


    def display(self):
        raise NotImplementedError



