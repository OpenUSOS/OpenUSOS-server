import os
import json

class Grades():

    def __init__(self, caller):
        self.caller = caller

    def get_grades(self):
        lista = []
        courses = self.caller.api.get('services/courses/user',  fields='course_editions[course_id|term_id]', active_terms_only = 'false')
        for term in courses["course_editions"]:
            courses_in_term = courses["course_editions"][term]
            for course in courses_in_term:
                info = self.caller.api.get('services/courses/course_edition' ,course_id = course["course_id"], term_id = course["term_id"],
                                    fields='course_name|term_id|grades[value_symbol|date_modified|modification_author]')
                    
                for grade_unit_id in info["grades"]["course_units_grades"]:
                    for exam_session in info["grades"]["course_units_grades"][grade_unit_id]:
                        grade = {}
                        grade["term"] = str(course["term_id"])
                        grade["name"] = info["course_name"]["pl"]
                        grade["author"] = info["grades"]["course_units_grades"][grade_unit_id][exam_session]["modification_author"]
                        if(grade["author"] is None):
                            grade["author"] = {}
                            grade["author"]["first_name"] = "-"
                            grade["author"]["last_name"] = "-"
                            grade["author"]["id"] = "-"
                        grade["value"] = info["grades"]["course_units_grades"][grade_unit_id][exam_session]["value_symbol"]
                        if(grade["value"] is None):
                            grade["value"] = "-"
                        grade["date"] = info["grades"]["course_units_grades"][grade_unit_id][exam_session]["date_modified"]
                        if(grade["date"] is None):
                            grade["date"] = "-"

                        try:
                            group = self.caller.api.get('services/groups/group', course_unit_id = grade_unit_id, group_number=1, fields='class_type_id')
                            grade["class_type"] = group["class_type_id"]
                        except:
                            grade["class_type"] = "WYK"
                        
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
    
    def get_tests_top(self):
        lista = []
        answ = self.caller.api.get('services/crstests/participant')
        for specific_term in answ["tests"]:
            term = {} #One specific term, eg 22/23 Z
            term["term_id"] = specific_term
            term["courses"] = [] #courses happening in a term
            for root_id in answ["tests"][specific_term]:
                course = {} #one specific course, eg ASD
                course["name"] = answ["tests"][specific_term][root_id]["course_edition"]["course_name"] #the name of a course
                course["nodes_id"] = root_id
                term["courses"].append(course) 
            lista.append(term)
        json_string = json.dumps(lista)
        return json_string
    
    def get_tests_node(self, node_id):
        node = {}
        info1 = self.caller.api.get('services/crstests/node2', node_id = int(node_id), fields = 'name|description|subnodes[id]')
        info2 = self.caller.api.get('services/crstests/task_node_details', id = int(node_id), fields = 'students_points|points_max')
        node["name"] = info1["name"]
        node["description"] = info1["description"]
        node["subnodes_ids"] = []
        if info2:
            node["points"] = info2["students_points"]["points"]
            node["points_max"] = info2["points_max"]
        else:
            node["points"] = "-"
            node["points_max"] = "-"

        for subnode in info1["subnodes"]:
            node["subnodes_ids"].append(subnode["id"])
        json_string = json.dumps(node)
        return json_string
    
    def get_tests_child(self, node_id):
            lista = []
            info1 = self.caller.api.get('services/crstests/node2', node_id = int(node_id), fields = 'subnodes[id]')
            for subnode in info1["subnodes"]:
                elem = {}
                info_sub_1 = self.caller.api.get('services/crstests/node2', node_id = int(subnode["id"]), fields = 'name|description')
                info_sub_2 = self.caller.api.get('services/crstests/task_node_details', id = int(subnode["id"]), fields = 'students_points|points_max')
                elem["id"] = subnode["id"]
                elem["name"] = info_sub_1["name"]
                elem["description"] = info_sub_1["description"]
                if info_sub_2:
                    elem["points"] = info_sub_2["students_points"]["points"]
                    elem["points_max"] = info_sub_2["points_max"]
                else:
                    elem["points"] = "-"
                    elem["points_max"] = "-"
                lista.append(elem)
            json_string = json.dumps(lista)
            return json_string



