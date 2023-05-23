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
    word_list.remove('')
    #Удаление найденных слов через анализ части речи
    for del_word in deletion_mas:
        word_list.remove(del_word)

    return word_list


def main():

    list = read_files()
    Id = 1
    count = 0

    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse')
    VO_patent_count = client.query('SELECT count() FROM db_patents.yandex_problem_solution').result_rows[0][0]
    IPC_patent_count = client.query('SELECT count() FROM db_patents.IPC_problem_solution').result_rows[0][0]

    for i in range(1, VO_patent_count):
        VO_result = client.query(f'SELECT Problem FROM db_patents.yandex_problem_solution WHERE Id = {i}')
        VO_problem = VO_result.result_rows[0][0]

        if VO_problem:
            VO_tmp = dict()
            VO_res = dict()
            for word in list:
                if word in VO_problem[0]:
                    index = VO_problem[0].find(word)
                    splitted_string = VO_problem[0][index:]
                    anl_string = splitted_string.split(',')[0]
                    print(anl_string)
                    doc = nlp(anl_string)
                    for sent in doc.sentences:
                        for a in sent.words:
                            VO_tmp[a.text] = {"deprel": a.deprel, "lemma": a.lemma}
                    for k in VO_tmp.keys():
                        if VO_tmp[k]["deprel"] in ["root", "nmod"]:
                            VO_res[k] = VO_tmp[k]["lemma"]



        for c in range(1, IPC_patent_count):
            IPC_result = client.query(f'SELECT Problem FROM db_patents.IPC_problem_solution WHERE Id = {i}')
            IPC_asignee = client.query(f'SELECT Asignee FROM db_patents.IPC_google_patents WHERE Id = {i}').result_rows[0][0]
            IPC_problem = IPC_result.result_rows[0][0]
            if IPC_problem:
                IPC_tmp = dict()
                IPC_res = dict()
                for word in list:
                    if word in IPC_problem[0]:
                        IPC_index = IPC_problem[0].find(word)
                        IPC_splitted_string = IPC_problem[0][IPC_index:]
                        IPC_anl_string = IPC_splitted_string.split(',')[0]
                        print(IPC_anl_string)

                        IPC_doc = nlp(IPC_anl_string)
                        for sent in IPC_doc.sentences:
                            for a in sent.words:
                                IPC_tmp[a.text] = {"deprel": a.deprel, "lemma": a.lemma}
                        for k in IPC_tmp.keys():
                            if IPC_tmp[k]["deprel"] in ["root", "nmod"]:
                                IPC_res[k] = {"lemma": IPC_tmp[k]["lemma"]}

                for l in IPC_res.keys():
                    if IPC_tmp[l]["lemma"] in VO_res:
                        count += 1

                if count > 3:
                    sim_probs = ['fff', 'ddd']
                    row = [Id, IPC_asignee, IPC_problem[0], sim_probs]
                    data = [row]
                    client.insert('Potential_partners', data,
                                  column_names=['Id', 'Organisation_name', 'Problems', 'Similar_problems'], database="db_patents")
                    Id += 1
            #print(f'analyzed patent #{c}')


if __name__ == "__main__":
    main()

