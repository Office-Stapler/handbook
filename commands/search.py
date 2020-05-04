import bs4
import json
import requests

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
    url = 'https://www.handbook.unsw.edu.au/undergraduate/courses/2020/'
    fac_code = query[0:4]
    with open('subjectinfo.json', 'r') as f:
        subjects = json.load(f)
    if fac_code not in subjects:
        return None
    
    if query not in [x[0] for x in subjects[fac_code]]:
        return subjects[fac_code]
    for subject in subjects[fac_code]:
        if subject[0] == query:
            name = subject[1]
    page = requests.get(url + query).text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    info = soup.find_all('div', class_='readmore__wrapper')
    overview = info[0].get_text().strip()
    offering = soup.find_all('p', class_='')

    for offer in offering:
        if 'Term' in offer.get_text():
            offering = offer.get_text()
            break
    return {
        'overview': overview,
        'terms': offering,
        'name': name
    }


