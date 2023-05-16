import stanza
from database import client
import csv


def read_files():
    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse')
    tmp = dict()
    word_list = []
    deletion_mas = []
    with open('dataset.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            tmp_list = row[1].split(";")
            for word in tmp_list:
                if word != '':
                    word = word.split(" ")
                    if word[0] not in word_list:
                        word_list.append(word[0])

    with open('dataset_1.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            tmp_list = row[1].split(";")
            for word in tmp_list:
                if word != '':
                    word = word.split(" ")
                    if word[0] not in word_list:
                        word_list.append(word[0])

    file = open("sentences.txt")
    for line in file:
        sent  = line.split(",")
        for s in sent:
            tmp_list = row[1].split(";")
            for word in tmp_list:
                if word != '':
                    word = word.split(" ")
                    if word[0] not in word_list:
                        word_list.append(word[0])

    #Нахождение лишних слов с помощью поиска частей речи
    for f in word_list:
        doc = nlp(f)
        for sent in doc.sentences:
            for word in sent.words:
                tmp[word.text] = {"upos": word.upos, "lemma": word.lemma}
                f = tmp[word.text]["lemma"]
    for k in tmp.keys():
        if (tmp[k]["upos"] in ["ADJ", "ADV","PUNCT"]):
            deletion_mas.append(k)

    #Удаление лишних слов из списка
    #Удаление вручную
    deletion_mas.remove(",")
    word_list.remove("автоматизированное")
    word_list.remove("сбор,")
    word_list.remove("обеспеченин")
    word_list.remove("полученин")
    #Удаление найденных слов через анализ части речи
    for del_word in deletion_mas:
        word_list.remove(del_word)

    #print(word_list)
    for a in word_list:
        print(a)
    #return word_list ADJ ADV PUNCT


def main():

    read_files()
    Id = 1

    test = "Задачей изобретения является обеспечение возможности получения арматурной проволоки с повышенными физико-механическими и служебными свойствами из низкоуглеродистой стали, снижение энергоемкости производственного процесса, повышение точности профиля проволоки посредством регулирования его размера и конфигурации на последнем этапе ее изготовления."
    tmp = dict()
    res = dict()
    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse')
    patent_count = client.query('SELECT count() FROM db_patents.IPC_problem_solution').result_rows[0][0]

    for i in range(1, patent_count):
        result = client.query(f'SELECT Problem FROM db_patents.IPC_problem_solution WHERE Id = {i}')
        problem = result.result_rows[0][0]
        doc = nlp(test)
        print(doc)
        for sent in doc.sentences:
            for word in sent.words:
                tmp[word.text] = {"head": sent.words[word.head - 1].text, "dep": word.deprel, "id": word.id}
            for k in tmp.keys():
                nmod_1 = ""
                nmod_2 = ""
                if (tmp[k]["dep"] in ["obl", "nmod"]):
                    res[k] = {"head": tmp[k]["head"]}
            print(tmp)
            print(res)



if __name__ == "__main__":
    main()

