import json

def verify_time(time):
    try:
        year = int(time[:2])
        term = int(time[-1])
        if not 0 <= term <= 3:
            return False
    except ValueError:
        return False
    return len(time) == 4

# -1 is invalid time
# -2 is person not found
# -3 too many subjects
# 1 person had been added
# 0 is no issues
codes = {
    -1: 'Invalid time',
    -2: 'Person not found',
    -3: 'Too many subjects',
    -4: 'Subject not found',
    -5: 'Subject already added for this term',
    -6: 'Too many characters',
    0: 'Success',
    1:'Person had been added'
}
def add_subject(subject, time, name):
    if not verify_time(time):
        return -1
    if len(subject) > 8:
        return -6
    with open('data/timetables.json', 'r') as f:
        planner = json.load(f)
    return_code = -3
    if name not in planner:
        planner[name] = {
            time: [subject]
        }
        return_code = 1
    elif time not in planner[name]:
        planner[name][time] = [subject]
        return_code = 0
    elif len(planner[name][time]) < 3:
        if time not in planner[name]:
            planner[name][time] = [subject]
        else:
            if subject in planner[name][time]:
                return -5
            planner[name][time].append(subject)
        return_code = 0

    with open('data/timetables.json', 'w') as f:
        json.dump(planner, f, indent = 4)

    return return_code

def remove_subject(subject, time, name):
    if not verify_time(time):
        return -1

    with open('data/timetables.json', 'r') as f:
        planner = json.load(f)
    print(name)
    print(planner)
    if name not in planner:
        return -2

    subjects = planner[name][time]
    size = len(subjects)
    found = False
    if size != 0:
        for i in range(size):
            if subjects[i] == subject:
                subjects.pop(i)
                Found = True
                break
    with open('data/timetables.json', 'w') as f:
        json.dump(planner, f, indent = 4)

    return 0 if Found else -4

def get_subjects(time, name):
    if not verify_time(time):
        return []
    
    with open('data/timetables.json', 'r') as f:
        planner = json.load(f)
    
    if name not in planner:
        return []
    
    if time not in planner[name]:
        return []
    
    return planner[name][time]

def get_subjects_year(year, name):
    if len(year) != 2:
        return []
    with open('data/timetables.json', 'r') as f:
        planner = json.load(f)
    
    if name not in planner:
        return []

    subjects = {

    }
    for term in planner[name]:
        if term.startswith(year):
            subjects[term] = planner[name][term]

    return subjects

    

