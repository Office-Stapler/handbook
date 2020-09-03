import bs4
import json
import requests

SUBJECT_INFO = {}

UGRAD_API = 'https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_psubject%20+unsw_psubject.studyLevelURL:undergraduate%20+unsw_psubject.implementationYear:2020%20+unsw_psubject.code:'
PGRAD_API = "https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_psubject%20+unsw_psubject.studyLevelURL:postgraduate%20+unsw_psubject.implementationYear:2020%20+unsw_psubject.code:"

UGRAD_URL = "https://www.handbook.unsw.edu.au/undergraduate/courses/2020/"
PGRAD_URL = 'https://www.handbook.unsw.edu.au/postgraduate/courses/2020/'


class InvalidRequestException(Exception):
    pass

def find_prereq(prereqs):
    finalList = []
    for prereq in prereqs:
        soup = bs4.BeautifulSoup(prereq["description"], 'html.parser')
        finalList.append(soup.getText())
    return finalList

def parse_subject_info():
    """Parses the course information from JSON into a Python dict.

    Returns:
        array[array[dict]]: [{
            faculty_name: [
                {
                    "code": 8 character course code,
                    "name": Full course name,
                    "uoc": Unit of credits
                }
            ]
        }]
    """

    subject_info = {"faculties": set()}

    with open('data/subjectinfo.json', 'r') as f:
        subjects = json.load(f)

    for faculty in subjects:
        subject_info[faculty] = subjects[faculty]
        subject_info["faculties"].add(faculty)

    return subject_info


def get_handbook_details(query):
    """Gets a more detailed description of a course from the handbook. 

    Args:
        query (str) - course code (possibly partial) to search the handbook.

    Returns:
        tuple: (name, overview, offering, url, prereqs)
    """
    url = UGRAD_API + query.upper()
    rq = requests.get(url)
    full = rq.json()["contentlets"]
    if len(full) == 0:
        raise InvalidRequestException("Invalid course code")

    details = json.loads(full[0]["data"])
    
    name = details["title"]

    soup = bs4.BeautifulSoup(details["description"], 'html.parser')
    overview = soup.getText()

    offering = details["offering_detail"]
    terms = list(map(str.strip, offering["offering_terms"].split(',')))
    terms.sort()

    prereqs = find_prereq(details["enrolment_rules"])
    return (name, overview, terms, UGRAD_URL + query, prereqs)

def search(query):
    ''' 
    Args:
        query (str) - course code (possibly partial) to search the handbook.
    
    Returns: 
        dict: {
            'overview': Course overview,
            'terms': Course offering terms,
            'name': Course name
        }

        None if faculty code is not found.
        list if faculty code found, but course code not found.
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
        return [subject["code"] for subject in subjects[faculty_code]]

    try:
        name, overview, offering, url, prereq = get_handbook_details(query)
    except InvalidRequestException:
        return []

    return {
        'overview': overview,
        'terms': offering,
        'name': name,
        'prereq': prereq,
        'url': url
    }

if __name__ == '__main__':
    print(search("dcsdcdkop"))