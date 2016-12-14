import logging
from random import randint
import schedule_manager as manager
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch_skill():
    welcome_msg = render_template('welcome_new_user')
    userid = str(session.user.userId)

    if manager.master_list.has_key(userid):
        welcome_msg = render_template('welcome_returning_user')
        print('returning user')
    else:
        manager.create_student(userid)

    return question(welcome_msg)

@ask.intent("AddIntent", convert={'Type': str, 'Name': str, 'Date': 'date'}, mapping = {'assignment_type' : 'Type'})
def add_assignment(assignment_type, Name, Date):
    print assignment_type
    print Name
    print Date
    userid = str(session.user.userId)
    manager.add_assignment(userid, assignment_type, Name + assignment_type, Date)
    response = render_template('added_assignment', name=Name, type=assignment_type, date=Date)

    return question(response)

@ask.intent("NextAssignmentIntent")
def next_assignment():
    userid = str(session.user.userId)
    assignment_to_do = manager.find_next_assignment(userid, 'all')
    Name = assignment_to_do[0]
    Date = assignment_to_do[1][1]
    response = render_template('next_assignment', name=Name, date=Date)

    return question(response)

@ask.intent("AMAZON.StopIntent")
def stop():
    response = render_template('stop')
    return statement(response)

# @ask.intent("DojoInfoIntent")
# def dojo_info():
#     response = render_template("dojo_info_template")
#     return statement(response)

# @ask.intent("DojoStaffIntent")
# def dojo_staff():
#     response = render_template("invalid_city")

#     return statement(response)

# @ask.intent("DojoStackIntent", convert={'City': str})
# def dojo_stacks(City):
#     response = ''
#     if City == "San Jose":
#         response = render_template("san_jose_stacks", city=City)
#     elif City == "Seattle":
#         response = render_template("seattle_stacks", city=City)
#     elif City == "Chicago":
#         response = render_template("chicago_stacks", city=City)
#     elif City == "Dallas":
#         response = render_template("dallas_stacks", city=City)
#     elif City == "Burbank":
#         response = render_template("burbank_stacks", city=City)
#     elif City == "Washington":
#         response = render_template("washington_stacks", city=City)
#     else:
#         response = render_template("invalid_city")

#     return statement(response)

# @ask.intent("DojoInstructorIntent", convert={'City': str})
# def dojo_instructors(City):
#     response = ''
#     if City == "San Jose":
#         response = render_template("san_jose_instructors", city=City)
#     elif City == "Seattle":
#         response = render_template("seattle_instructors", city=City)
#     elif City == "Chicago":
#         response = render_template("chicago_instructors", city=City)
#     elif City == "Dallas":
#         response = render_template("dallas_instructors", city=City)
#     elif City == "Burbank":
#         response = render_template("burbank_instructors", city=City)
#     elif City == "Washington":
#         response = render_template("washington_instructors", city=City)
#     else:
#         response = render_template("invalid_city")

#     return statement(response)


# @ask.intent("AMAZON.HelpIntent")
# def dojo_help():
#     response = render_template("help_template")
#     return question(response)

# @ask.intent("AMAZON.StopIntent")
# def dojo_stop():
#     response = render_template("stop_template")
#     return statement(response)


if __name__ == '__main__':

    app.run(debug=True)
