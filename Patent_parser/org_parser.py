import requests
import re
import csv
from bs4 import BeautifulSoup

url = "https://promtorg.volgograd.ru/current-activity/promyshlennost/list/map/"
page = requests.get(url, verify = False)
soup = BeautifulSoup(page.text, 'html.parser')
root = soup.find_all("table", {"class" : "tableclass"})
organisations = []
for row in root[0].tbody.findAll('tr'):
    org_name = row.findAll('td')[0].contents[0]
    organisations.append(org_name)
print(organisations)

# abbreviations = ["ЗАО","ООО","ОАО","Филиал","ФЛ","ФГУП","ВОЗ","МУП","АУ","МБУ","МАУ","АМУ","МУ"
#          "ЛК","ГБУК"]
# excluded_symbols = ['"',"»","«"]
# abbreviations.extend(excluded_symbols)
# abbreviation_pattern = "|".join(abbreviations)
# print(abbreviation_pattern)
#
# organisations = [re.sub(abbreviation_pattern, '', organisation).strip() for organisation in organisations]
# print(organisations)

# open the file in the write mode
with open('Parsers/organisations.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f,delimiter = "\n")
    writer.writerow(organisations)