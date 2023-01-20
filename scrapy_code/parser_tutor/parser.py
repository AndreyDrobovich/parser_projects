import requests

import pandas as pd

from bs4 import BeautifulSoup as bs

URl_TEMPLATE = 'https://www.work.ua/ru/jobs-odesa/?page=2'
FILE_NAME = 'result.csv'


def parse(url):
    result_list = {'href': [], 'title': [], 'about': []}
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    vacancies_names = soup.find_all('h2', class_='')[:14]
    vacancies_info = soup.find_all('p', class_='overflow')
    for name in vacancies_names:
        result_list['href'].append('https://www.work.ua'+name.a['href'])
        result_list['title'].append(name.a['title'])
    for info in vacancies_info:
        result_list['about'].append(info.text)
    return result_list


df = pd.DataFrame(data=parse(URl_TEMPLATE))
print(df)
df.to_csv(FILE_NAME)
