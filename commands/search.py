import bs4
import json
import requests

SUBJECT_INFO = {}

HANDBOOK_URL = 'https://www.handbook.unsw.edu.au/undergraduate/courses/2020/'


def parse_subject_info():
    subject_info = {"faculties": set()}

    with open('subjectinfo.json', 'r') as f:
        subjects = json.load(f)

    for faculty in subjects:
        faculty_courses = []
        for subject in subjects[faculty]:
            faculty_courses.append({
                "code": subject[0],
                "name": subject[1],
                "uoc": subject[2] 
            })
        subject_info[faculty] = faculty_courses
        subject_info["faculties"].add(faculty)

    return subject_info


def get_handbook_details(query):
    """
    Arguments: query - A string that will be used to search the handbook
    Return:
    Tuple: (overview, offering)
    """
    page = requests.get(HANDBOOK_URL + query).text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    info = soup.find_all('div', class_='readmore__wrapper')
    overview = info[0].get_text().strip()
    offering = soup.find_all('p', class_='')

    for offer in offering:
        if 'Term' in offer.get_text():
            offering = offer.get_text()
            break

    return overview, offering


def search(query):
    ''' 
        Arguments: query - A string that will be used to search the handbook
        Return: 
        Dictionary {
            'overview': Course overview,
            'terms': Course offering terms,
            'name': Course name
        }
        If the subject faculty code is not found it returns None,
        if the subject faculty code is found but the course code isn't it returns the list of courses
    '''

    query = query.upper()
    faculty_code = query[0:4]

    global SUBJECT_INFO
    if not SUBJECT_INFO:
        SUBJECT_INFO = parse_subject_info()
    subjects = SUBJECT_INFO

    if faculty_code not in SUBJECT_INFO["faculties"]:
        return None
    
    if query not in [subject["code"] for subject in subjects[faculty_code]]:
        return [(subject["code"], subject["name"], subject["uoc"])
                for subject in subjects[faculty_code]]
        
    for subject in subjects[faculty_code]:
        if subject["code"] == query:
            name = subject["name"]

    overview, offering = get_handbook_details(query)

    return {
        'overview': overview,
        'terms': offering,
        'name': name
    }
