import os
import logging
from random import randint
import schedule_manager as manager
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch_skill():
    welcome_msg = render_template('welcome_new_user')
    userid = str(session.user.userId)

    if manager.master_list.has_key(userid):
        welcome_msg = render_template('welcome_returning_user')
    else:
        manager.create_student(userid)

    return statement(welcome_msg)

@ask.intent("AddIntent", convert={'Type': str, 'Name': str, 'Date': 'date'}, mapping = {'assignment_type' : 'Type'})
def add_assignment(assignment_type, Name, Date):
    userid = str(session.user.userId)

    if(assignment_type):
        if isTest(assignment_type):
            assignment_type = 'test'

        if isEssay(assignment_type):
            assignment_type = 'essay'

        session.attributes['type'] = assignment_type
    if(Name):
        session.attributes['name'] = Name
    if(Date):
        session.attributes['date'] = str(Date)

    try:
        session.attributes['type']
    except:
        return question(render_template('unknown_type'))

    try:
        session.attributes['name']
    except:
        return question(render_template('unknown_name'))

    try:
        session.attributes['date']
    except:
        return question(render_template('unknown_date'))
    
    name_to_add = session.attributes['name']
    type_to_add = session.attributes['type']
    date_to_add = session.attributes['date']
    text = render_template('added_assignment', name=name_to_add, type=type_to_add, date=date_to_add)
    response = statement(text)
    
    try:
        manager.add_assignment(userid, type_to_add, name_to_add +' '+ type_to_add, date_to_add)
    except:
        return statement(render_template('assignment_exists'))

    return response

@ask.intent("NextAssignmentIntent")
def next_assignment():
    userid = str(session.user.userId)

    assignment_to_do = manager.find_next_assignment(userid, 'all')

    if(assignment_to_do):
        Name = assignment_to_do[0]
        Date = assignment_to_do[1][1]
        response = render_template('next_assignment', name=Name, date=Date)

    else:
        return statement(render_template('all_complete'))

    return statement(response)

@ask.intent("NextTypeIntent", convert = {"Type": str}, mapping = {'assignment_type' : 'Type'})
def next_type_assignment(assignment_type):
    userid = str(session.user.userId)

    if isTest(assignment_type):
        assignment_type = 'test'

    if isEssay(assignment_type):
        assignment_type = 'essay'

    assignment_to_do = manager.find_next_assignment(userid, assignment_type)

    if(assignment_to_do):
        Name = assignment_to_do[0]
        Date = assignment_to_do[1]
        response = render_template('next_assignment', type='assignment_type', name=Name, date=Date)

    else:
        return statement(render_template('all_complete'))

    return statement(response)

@ask.intent("CompletedAssignmentIntent", convert = {"Type": str, "Name": str}, mapping = {'assignment_type' : 'Type'})
def mark_complete(assignment_type, Name):
    userid = str(session.user.userId)

    if(assignment_type):
        if isTest(assignment_type):
            assignment_type = 'test'

        if isEssay(assignment_type):
            assignment_type = 'essay'

        session.attributes['type'] = assignment_type
    
    if(Name):
        session.attributes['name'] = Name

    try:
        session.attributes['type']
    except:
        return question(render_template('unknown_args_complete'))

    try:
        session.attributes['name']
    except:
        return question(render_template('unknown_args_complete'))

    name_to_add = session.attributes['name']
    type_to_add = session.attributes['type']

    assignment_name = name_to_add +" "+type_to_add

    
    if(manager.mark_completed(userid, assignment_name)):
        return statement("The next " + assignment_name +  " has been marked as completed")
    else:
        return statement(assignment_name + " isn't on your schedule")

@ask.intent("NotCompletedAssignmentIntent", convert = {"Type": str, "Name": str}, mapping = {'assignment_type' : 'Type'})
def mark_incomplete(assignment_type, Name):
    userid = str(session.user.userId)
    
    if(assignment_type):
        if isTest(assignment_type):
            assignment_type = 'test'

        if isEssay(assignment_type):
            assignment_type = 'essay'

        session.attributes['type'] = assignment_type
    
    if(Name):
        session.attributes['name'] = Name

    try:
        session.attributes['type']
    except:
        return question(render_template('unknown_args_non_complete'))

    try:
        session.attributes['name']
    except:
        return question(render_template('unknown_args_non_complete'))

    name_to_add = session.attributes['name']
    type_to_add = session.attributes['type']

    assignment_name = name_to_add +" "+type_to_add


    if(manager.mark_not_completed(userid, assignment_name)):
        return statement("The next " + assignment_name +  " has been marked as not completed")
    else:
        return statement(assignment_name + " isn't on your schedule")

@ask.intent("NextNameIntent", convert = {"Type": str, "Name": str}, mapping = {'assignment_type' : 'Type'})
def next_name_assignment(assignment_type, Name):
    userid = str(session.user.userId)
    
    if(assignment_type):
        if isTest(assignment_type):
            assignment_type = 'test'

        if isEssay(assignment_type):
            assignment_type = 'essay'

        session.attributes['type'] = assignment_type
    
    if(Name):
        session.attributes['name'] = Name

    try:
        session.attributes['type']
    except:
        return question(render_template('unknown_args_next_name'))

    try:
        session.attributes['name']
    except:
        return question(render_template('unknown_args_next_name'))

    name_to_add = session.attributes['name']
    type_to_add = session.attributes['type']

    assignment_name = name_to_add +" "+type_to_add

    assignment = ''
    try:
        assignment = manager.find_assignment(userid, assignment_name)
    except Exception as e:
        return statement("I couldn't find an assignment with that name")

    return statement(assignment_name + " is scheduled for " + str(assignment[1]))

@ask.intent("AMAZON.StopIntent")
def stop():
    response = render_template('stop')
    return statement(response)

@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement(render_template('stop'))

def isTest(name):
    test_types = ['test', 'final', 'midterm', 'mid term', 'mid-term', 'exam']
    if name in test_types:
        return True

    return False

def isEssay(name):
    essay_types = ['essay',  'paper']
    if name in  essay_types:
        return True

    return False

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
