import json
subjects = None

def name_search(name):
    global subjects
    if not subjects:
        with open('subjectinfo.json', 'r') as f:
            subjects = json.load(f)
    found = []
    for faculty in subjects:
        for subject in subjects[faculty]:
            if name.lower() in subject['name'].lower():
                found.append(subject)
    return found

if __name__ == '__main__':
    found = name_search(input())
    for subject in found:
        print(subject['code'], subject['name'])