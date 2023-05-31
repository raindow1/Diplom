import stanza
from Database.database import client
import csv
from ruwordnet import RuWordNet


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
    wn = RuWordNet()
    VO_tmp = dict()
    VO_res_root = dict()
    VO_res_nmod = dict()
    VO_third_nmod = dict()
    VO_nmod_hyponyms = []
    VO_third_hyponyms = []


    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse')
    VO_patent_count = client.query('SELECT count() FROM db_patents.yandex_problem_solution').result_rows[0][0]
    IPC_patent_count = client.query('SELECT count() FROM db_patents.IPC_problem_solution').result_rows[0][0]

    for i in range(1, VO_patent_count):
        VO_result = client.query(f'SELECT Problem FROM db_patents.yandex_problem_solution WHERE Id = {i}')
        VO_problem = VO_result.result_rows[0][0]

        VO_res_root.clear()
        VO_res_nmod.clear()
        VO_third_nmod.clear()
        VO_tmp.clear()
        VO_nmod_hyponyms.clear()
        VO_third_hyponyms.clear()

        if VO_problem:
            for word in list:
                if word in VO_problem[0]:
                    index = VO_problem[0].find(word)
                    splitted_string = VO_problem[0][index:]
                    anl_string = splitted_string.split(',')[0]
                    #print(anl_string)
                    doc = nlp(anl_string)
                    #print(doc)
                    for sent in doc.sentences:
                        for a in sent.words:
                            VO_tmp[a.text] = {"deprel": a.deprel, "lemma": a.lemma, "id": a.id, "head":a.head}
                    for k in VO_tmp.keys():
                        if VO_tmp[k]["deprel"] in ["root"]:
                            VO_res_root[k] = {"lemma": VO_tmp[k]["lemma"], "id": VO_tmp[k]["id"]}
                            VO_root_id = VO_res_root[k]["id"]
                        if VO_tmp[k]["deprel"] in ["nmod"] and VO_tmp[k]["head"] == VO_root_id:
                            VO_res_nmod[k] = {"lemma": VO_tmp[k]["lemma"]}
                            VO_second_nmod_id = VO_tmp[k]["id"]
                        if VO_tmp[k]["deprel"] in ["nmod"] and VO_tmp[k]["head"] == VO_second_nmod_id:
                            VO_third_nmod[k] = {"lemma": VO_tmp[k]["lemma"]}

                    for VO_key_nmod in VO_res_nmod.keys():
                        try:
                            VO_nmod_synsets = wn.get_senses(VO_res_nmod[VO_key_nmod]["lemma"])[0].synset.hypernyms
                            VO_nmod_hyponyms = VO_nmod_synsets[0].title.split(",")
                        except (KeyError, IndexError):
                            VO_nmod_synsets = ""
                        VO_nmod_hyponyms.append(VO_res_nmod[VO_key_nmod]["lemma"])

                    for VO_key_third_nmod in VO_third_nmod.keys():
                        try:
                            VO_third_synsets = wn.get_senses(VO_res_nmod[VO_key_third_nmod]["lemma"])[0].synset.hypernyms
                            VO_third_hyponyms = VO_third_synsets[0].title.split(",")
                        except (KeyError, IndexError):
                            VO_third_synsets = ""
                        VO_third_hyponyms.append(VO_third_nmod[VO_key_third_nmod]["lemma"])


                    # print(VO_res_root)
                    # print(VO_res_nmod)
                    # print(VO_third_nmod)
                    # print(VO_nmod_hyponyms)
                    # print(VO_third_hyponyms)




        for c in range(1, IPC_patent_count):
            IPC_result = client.query(f'SELECT Problem FROM db_patents.IPC_problem_solution WHERE Id = {c}')
            IPC_asignee = client.query(f'SELECT Asignee FROM db_patents.IPC_google_patents WHERE Id = {c}').result_rows[0][0]
            IPC_problem = IPC_result.result_rows[0][0]
            if IPC_problem:
                IPC_tmp = dict()
                IPC_res_root = dict()
                IPC_res_nmod = dict()
                IPC_third_nmod = dict()
                IPC_nmod_hyponyms = []
                IPC_third_hyponyms = []

                for word in list:
                    if word in IPC_problem[0]:
                        IPC_index = IPC_problem[0].find(word)
                        IPC_splitted_string = IPC_problem[0][IPC_index:]
                        IPC_anl_string = IPC_splitted_string.split(',')[0]
                        #print(IPC_anl_string)
                        IPC_doc = nlp(IPC_anl_string)
                        for sent in IPC_doc.sentences:
                            for a in sent.words:
                                IPC_tmp[a.text] = {"deprel": a.deprel, "lemma": a.lemma, "id": a.id, "head": a.head}
                        for k in IPC_tmp.keys():
                            if IPC_tmp[k]["deprel"] in ["root"]:
                                IPC_res_root[k] = {"lemma": IPC_tmp[k]["lemma"], "id": IPC_tmp[k]["id"]}
                                IPC_root_id = IPC_res_root[k]["id"]
                            if IPC_tmp[k]["deprel"] in ["nmod"] and IPC_tmp[k]["head"] == IPC_root_id:
                                IPC_res_nmod[k] = {"lemma": IPC_tmp[k]["lemma"]}
                                IPC_second_nmod_id = IPC_tmp[k]["id"]
                            if IPC_tmp[k]["deprel"] in ["nmod"] and IPC_tmp[k]["head"] == IPC_second_nmod_id:
                                IPC_third_nmod[k] = {"lemma": IPC_tmp[k]["lemma"]}

                        for IPC_key_nmod in IPC_res_nmod.keys():
                            try:
                                IPC_nmod_synsets = wn.get_senses(IPC_res_nmod[IPC_key_nmod]["lemma"])[0].synset.hypernyms
                                IPC_nmod_hyponyms = IPC_nmod_synsets[0].title.split(",")
                            except (KeyError,IndexError):
                                IPC_nmod_synsets = ""
                            IPC_nmod_hyponyms.append(IPC_res_nmod[IPC_key_nmod]["lemma"])

                        for IPC_key_third_nmod in IPC_third_nmod.keys():
                            try:
                                IPC_third_synsets = wn.get_senses(IPC_res_nmod[IPC_key_third_nmod]["lemma"])[0].synset.hypernyms
                                IPC_third_hyponyms = IPC_third_synsets[0].title.split(",")
                            except (KeyError, IndexError):
                                IPC_third_synsets = ""
                            IPC_third_hyponyms.append(IPC_third_nmod[IPC_key_third_nmod]["lemma"])

                for root_key in VO_res_root:
                    if root_key in IPC_res_root:
                        count += 1
                for nmod_key in VO_nmod_hyponyms:
                    if nmod_key in IPC_nmod_hyponyms:
                        count += 1
                for third_nmod_key in VO_third_hyponyms:
                    if third_nmod_key in IPC_third_hyponyms:
                        count += 1

                # if count >= 3:
                #     sim_probs = ['fff', 'ddd']
                #     row = [Id, IPC_asignee, IPC_problem[0], sim_probs]
                #     data = [row]
                #     client.insert('Potential_partners', data,
                #                   column_names=['Id', 'Organisation_name', 'Problems', 'Similar_problems'],
                #                   database="db_patents")
                #     Id += 1

                    print(IPC_res_root)
                    # print(IPC_res_nmod)
                    # print(IPC_third_nmod)
                    print(IPC_nmod_hyponyms)
                    print(IPC_third_hyponyms)
                    IPC_res_root.clear()
                    IPC_res_nmod.clear()
                    IPC_third_nmod.clear()
                    IPC_tmp.clear()
                    IPC_nmod_hyponyms.clear()
                    IPC_third_hyponyms.clear()

            print(f'analyzed patent #{c}')







if __name__ == "__main__":
    main()

