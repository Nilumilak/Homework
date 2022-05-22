import requests
import time
from pprint import pprint


def find_all_questions(days: int, *tags: str, hours: int = 0, minutes: int = 0) -> list:
    """
    :param tags: names of tags for searching.
                 find_all_questions(1, 'python'); find_all_questions(0, 'python', 'pandas', minutes=10)
    :param days: number of days
    :param hours: number of hours
    :param minutes: number of minutes
    :return: list of all questions with tags and links within the searching time --> [['question', ['tags'], 'link']

    """
    result = []
    last_post = time.time() - ((days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60))
    page = 0

    header = {'Content-Type': 'application/json'}

    while True:
        page += 1
        param = {
            'tagged': '; '.join(tags),
            'sort': 'creation',
            'site': 'stackoverflow',
            'pagesize': '30',
            'page': str(page),
            'order': 'desc'
        }
        respond = requests.get('https://api.stackexchange.com/2.3/questions', headers=header, params=param)
        time.sleep(2)
        for line in respond.json()['items']:
            last_created = line['creation_date']
            if last_created <= last_post:
                print('Success')
                return result
            result.append([line['title'], line['tags']])


pprint(find_all_questions(0, 'python', 'pandas', minutes=10))
