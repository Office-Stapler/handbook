import bs4
import json
import requests

SUBJECT_INFO = {}

API_SUFFIX = '%20+unsw_psubject.implementationYear:2020%20+unsw_psubject.code:'


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

def get_handbook_details(query, level):
    """Gets a more detailed description of a course from the handbook. 

    Args:
        query (str) - course code (possibly partial) to search the handbook.

    Returns:
        tuple: (name, overview, offering, url, prereqs, equivalents)
    """
    prefix = f"https://www.handbook.unsw.edu.au/api/content/render/false/query/+contentType:unsw_psubject%20+unsw_psubject.studyLevelURL:{level}"
    url = prefix + API_SUFFIX + query.upper()
    handbook_URL = f"https://www.handbook.unsw.edu.au"
    rq = requests.get(url)
    full = rq.json()["contentlets"]
    if len(full) == 0:
        if level == 'undergraduate':
            return get_handbook_details(query, 'postgraduate')
        elif level == "postgraduate":
            return get_handbook_details(query, "research")
        raise InvalidRequestException("Invalid course code")
    
    details = json.loads(full[0]["data"])

    name = details["title"]

    soup = bs4.BeautifulSoup(details["description"], 'html.parser')
    overview = soup.getText()

    offering = details["offering_detail"]
    terms = list(map(str.strip, offering["offering_terms"].split(',')))
    terms.sort()
    prereqs = find_prereq(details["enrolment_rules"])

    equivalents = []
    for equivalent in details["eqivalents"]:
        eqv_title = equivalent["assoc_title"]
        eqv_url = equivalent["assoc_url"]
        eqv_code = equivalent["assoc_code"]
        equivalents.append((eqv_title, eqv_url, eqv_code))

    return (name, overview, ", ".join(terms), handbook_URL + full[0]["urlMap"], prereqs, equivalents)

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

    try:
        name, overview, offering, url, prereq, equivalents = get_handbook_details(query, 'undergraduate')
    except InvalidRequestException:
        return [subject["code"] for subject in subjects[faculty_code]]

    return {
        'overview': overview,
        'terms': offering,
        'name': name,
        'prereq': prereq,
        'url': url,
        'equivalents': equivalents
    }

if __name__ == '__main__':
    print(get_handbook_details("ACCT1501", 'undergraduate'))