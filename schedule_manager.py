from collections import namedtuple
from datetime import date
import my_exceptions

"""
schedule is a namedtuple
each entry in tuple has an array with 2 elements
	0 shows completion. True is completed, False is incomplete
	1 shows date, as a datetime.date object
"""
schedule = namedtuple("schedule", "tests quizzes homeworks essays labs")

"""
tuple_map is a dictionary that matches assignment_type with index in the schedule namedtuple
"""
tuple_map = {'test': 0,
			 'quiz': 1,
			 'homework': 2,
			 'essay': 3,
			 'lab': 4}

"""
master_list contains the data of all students
key: student_name
value: array with two entries
	0 is schedule tuple
	1 is array of all assignments sorted by date
"""
master_list = {}

"""adds student to master_list with empty schedule
args:
	student_id: unique id of student to add to master list
returns
	nothing
exceptions
	student_already_exists, if the student_id is not unique
"""
def create_student(student_id):
	student_schedule = schedule(
		tests = {},
		quizzes = {},
		homeworks = {},
		essays = {},
		labs = {},
	)
	student_all_assignments = {}
	if(master_list.has_key(student_id)):
		raise my_exceptions.student_already_exists
	else:
		master_list[student_id] = [student_schedule, student_all_assignments]

"""adds assignment for a student
args
	student_id: unique id to add assigment under that student
	assignment_type: one of the 5 types declared in schedule namedtuple
	assignment_name: name of assignment from student
	due_date: due date given by student
returns
	nothing
exceptions
	assignment_already_exists: if assignment with same name exists for the student
"""
def add_assignment(student_id, assigntment_type, assignment_name, due_date):
	assignment_list = master_list[student_id][0][tuple_map[assigntment_type]]
	student_all_assignments = master_list[student_id][1]

	assigntment_info = [False, due_date]

	if(assignment_list.has_key(assignment_name)):
		raise my_exceptions.assignment_already_exists
	else:
		assignment_list[assignment_name] = due_date
		student_all_assignments[assignment_name] = assigntment_info


"""adds multiple assignments for a student in a set interval
args
	student_id: unique id to add assigment under that student
	assignment_type: one of the 5 types declared in schedule namedtuple
	assignment_name: name of assignment from student
	due_date: due date given by student
returns
	nothing
exceptions
	assignment_already_exists: if assignment with same name exists for the student
"""		
def add_assignment_interval(student_id, assigntment_type, assignment_name, due_date, interval, end_date):
    assignment_list = master_list[student_id][0][tuple_map[assigntment_type]]
        student_all_assignments = master_list[student_id][1]
        
        assigntment_info = [False, due_date]
        
        if(assignment_list.has_key(assignment_name)):
            raise my_exceptions.assignment_already_exists
        else:
            for x in range (0, end_date, interval):
                assignment_list[assignment_name] = due_date + x
               
		
"""provdes assignment due date and completion information
args
	student_id: unique id to add assigment under that student
	assignment_type: one of the 5 types declared in schedule namedtuple
returns
	array with due date and completion information
		0 index: boolean indicating completion of assignment
		1 index: date object containing due date
exceptions:
	assignment_not_found: if the assignment with given name is not found for student
"""
def find_assignment(student_id, assignment_name):
	assignment = None
	for i in master_list[student_id][1]:
		if i == assignment_name:
			assignment = master_list[student_id][1][i]

	if(assignment == None):
		raise my_exceptions.assignment_not_found
	
	return assignment

"""determines if assignment is completed
args
	student_id: unique id to add assigment under that student
	assignment_type: one of the 5 types declared in schedule namedtuple
returns
	boolean: True if completed, false otherwise
exceptions
	none
"""
def is_completed(student_id, assignment_name):
	assignment = find_assignment(student_id, assignment_name)
	
	return assignment[0]

"""marks assignment as completed
args
	student_id: unique id to add assigment under that student
	assignment_type: one of the 5 types declared in schedule namedtuple
returns
	nothing
exceptions
	none
"""
def mark_completed(student_id, assignment_name):
	assignment = find_assignment(student_id, assignment_name)

	assignment[0] = True

"""marks assignment as not completed
args
	student_id: unique id to add assigment under that student
	assignment_type: one of the 5 types declared in schedule namedtuple
returns
	nothing
exceptions
	none
"""
def mark_not_completed(student_id, assignment_name):
	assignment = find_assignment(student_id, assignment_name)

	assignment[0] = False

"""sorts a certain dictionary by date
args
	student_id: unique id to add assigment under that student
	list_type: can be 'all' or any of the assignment types in schedule namedtuple
returns
	sorted list version of given input
exceptions
	none
"""
def sort_by_date(student_id, list_type):
	student_assignments = master_list[student_id][0]
	if list_type == 'test':
		tests = student_assignments[tuple_map[list_type]]
		return _sort_kind(tests)
	elif list_type == 'quiz':
		quizzes = student_assignments[tuple_map[list_type]]
		return _sort_kind(quizzes)
	elif list_type == 'homework':
		homeworks = student_assignments[tuple_map[list_type]]
		return _sort_kind(homeworks)
	elif list_type == 'lab':
		labs = student_assignments[tuple_map[list_type]]
		return _sort_kind(labs)
	elif list_type == 'essay':
		essays = student_assignments[tuple_map[list_type]]
		return _sort_kind(essays)
	else:
		student_all_assignments = master_list[student_id][1]
		return _sort_for_all(student_all_assignments)

"""sorts all assignments part of student data
"""
def _sort_for_all(dict):
	if(len(dict) == 0):
		raise my_exceptions.empty_dictionary

	sorted_dict = sorted(dict.items(), key = lambda x: x[1][1])
	return sorted_dict

"""sorts certain type of assignment
"""
def _sort_kind(dict):
	if(len(dict) == 0):
		raise my_exceptions.empty_dictionary

	sorted_dict = sorted(dict.items(), key = lambda x: x[1])
	return sorted_dict
"""
TODO: support for certain type of assignment
"""
def find_next_assignment(student_id, list_type):
	if list_type == 'all':
		sorted_assignments = sort_by_date(student_id, list_type)
		for assignment in sorted_assignments:
			if assignment[1][0] == False:
				return assignment

def print_user_list():
	for i in master_list:
		print i

"""
TESTING
"""

create_student('test_student')
add_assignment('test_student', 'test', 'MAJOR EXAM 1', date(2016, 12, 17))
add_assignment('test_student', 'test', 'MAJOR EXAM 2', date(2016, 12, 13))
mark_completed('test_student', 'MAJOR EXAM 1')
add_assignment('test_student', 'test', 'MAJOR EXAM 3', date(2016, 12, 14))
mark_completed('test_student', 'MAJOR EXAM 3')
add_assignment('test_student', 'test', 'MAJOR EXAM 4', date(2016, 12, 16))
add_assignment('test_student', 'quiz', 'MINOR QUIZ 1', date(2016, 12, 18))
