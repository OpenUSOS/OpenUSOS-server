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


    def get_tests(self):
        lista = []
        answ = self.caller.api.get('services/crstests/participant')
        for specific_term in answ["tests"]:
            term = {} #One specific term, eg 22/23 Z
            term["term_id"] = specific_term
            term["courses"] = [] #courses happening in a term
            for root_id in answ["tests"][specific_term]:
                course = {} #one specific course, eg ASD
                course["name"] = answ["tests"][specific_term][root_id]["course_edition"]["course_name"] #the name of a course
                course["tests"] = [] #The tests in a course, like activity or kolos
                course_tests = self.caller.api.get('services/crstests/node2', node_id = root_id, fields = 'subnodes[id|name|description]')
                for course_test in course_tests["subnodes"]:
                    test = {} # a specific test.
                    test["name"] = course_test["name"] #name of a test
                    test["description"] = course_test["description"]
                    test_points = self.caller.api.get('services/crstests/task_node_details', id = course_test["id"], fields='students_points|points_max')
                    if(test_points):
                        test["points"] = test_points["students_points"]["points"]
                    else:
                        test["points"] = None

                    if(test_points):
                        test["points_max"] = test_points["points_max"]
                    else:
                        test["points_max"] = None

                    test["exercises"] = [] #list of all exercises, eg. a task in a test.
                    test_exercieses = self.caller.api.get('services/crstests/node2', node_id = course_test["id"], fields = 'subnodes[id|name|description]')
                    for test_exercise in test_exercieses["subnodes"]:
                        exercise = {}
                        exercise["name"] = test_exercise["name"]
                        exercise["description"] = test_exercise["description"]
                        exercise_points = self.caller.api.get('services/crstests/task_node_details', id = test_exercise["id"], fields='students_points|points_max')
                        if(exercise_points):
                            exercise["points"] = exercise_points["students_points"]["points"]
                        else:
                            exercise["points"] = None
                            
                        if(exercise_points):
                            exercise["points_max"] = exercise_points["points_max"]
                        else:
                            exercise["max_points"] = None
                        
                        test["exercises"].append(exercise)
                    course["tests"].append(test)
                term["courses"].append(course) 
            lista.append(term)
        json_string = json.dumps(lista)
        return json_string



