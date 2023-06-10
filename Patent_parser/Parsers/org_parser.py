import requests
import re
import csv
from bs4 import BeautifulSoup


def main():

    # Ссылка на сайт с организациями Волгоградской области
    url = "https://promtorg.volgograd.ru/current-activity/promyshlennost/list/map/"

    # Список со строками названий организаций
    organisations = []

    # Получение html-версти сайта
    page = requests.get(url, verify = False)

    # Поиск необходимого тега
    soup = BeautifulSoup(page.text, 'html.parser')
    root = soup.find_all("table", {"class" : "tableclass"})

    # Запись названий организаций в список
    for row in root[0].tbody.findAll('tr'):
        org_name = row.findAll('td')[0].contents[0]
        organisations.append(org_name)

    # Запись названий организаций в CSV-файл
    with open('../Data/organisations.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f,delimiter = "\n")
        writer.writerow(organisations)


if __name__ == "__main__":
    main()