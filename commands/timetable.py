import requests
import bs4
import datetime
def timetable(course):
    year = datetime.datetime.now().year
    timetable_url = f'http://timetable.unsw.edu.au/{year}'
    if requests.get(timetable_url).status_code != 200:
        year -= 1
    url = f'http://timetable.unsw.edu.au/{year}/{course}.html'
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    rows = soup.findAll(True, {
        'class': ['rowLowlight', 'rowHighlight']
    })
    times = {
        'T1': [],
        'T2': [],
        'T3': []
    }
    periods = ['T1', 'T2', 'T3']
    for row in rows:
        info = row.text.strip().split('\n')
        if info[1] in periods:
            period = info[1]
            del info[1]
            times[period].append(info)
    return times

if __name__ == '__main__':
    print(timetable('ENGG2000'))