from Database.database import client
from deep_translator import GoogleTranslator
import time


def create_chunks(corpus, max_chunk_size):
    chunks = [corpus[i:i + max_chunk_size] for i in range(0, len(corpus), max_chunk_size)]
    return chunks


def translate(field, max_chunk_size):
    #translator = Translator(to_lang='ru', from_lang='en')
    if len(field) > max_chunk_size:
        results_list = []
        concatenated_result = ""

        original_chunks = create_chunks(field, max_chunk_size)
        #original_chunks = list(sentenize(field))
        for i in original_chunks:
            r = GoogleTranslator(source='en', target='ru').translate(text=i)
            time.sleep(3)
            results_list.append(r)

        for i in results_list:
            concatenated_result += i

        return concatenated_result
    else:
        res = GoogleTranslator(source='en', target='ru').translate(text=field)
        time.sleep(10)
        return res


def main():
    Id = 2707

    max_chunk_size = 4000
    patent_count = client.query('SELECT count() FROM db_patents.IPC_google_patents').result_rows[0][0]

    for i in range(2708, patent_count):
        index = client.query(f'SELECT Index FROM db_patents.IPC_google_patents WHERE Id = {i}').result_rows[0][0]
        result = client.query(f'SELECT Description, Abstract FROM db_patents.IPC_google_patents WHERE Id = {i}')
        solution = client.query(f'SELECT Title FROM db_patents.IPC_google_patents WHERE Id = {i}').result_rows[0][0]
        description = result.result_rows[0][0]
        abstract = result.result_rows[0][1]
        if 'RU' not in index:
            translated_solution = translate(solution, max_chunk_size)
            #print(translated_solution)
            translated_description = translate(description, max_chunk_size)
            #print(translated_description)
            translated_abstract = translate(abstract, max_chunk_size)
            #print(translated_abstract)

            row = [Id, translated_abstract, translated_description, i, translated_solution]
            data = [row]
            client.insert('translated_IPC_patents', data,
                          column_names=['Id', 'Abstract', 'Description', 'Patent_id', 'Solution'], database="db_patents")
        else:
            row = [Id, abstract, description, i, solution]
            data = [row]
            client.insert('translated_IPC_patents', data,
                          column_names=['Id', 'Abstract', 'Description', 'Patent_id', 'Solution'],
                          database="db_patents")
        Id += 1


if __name__ == "__main__":
    main()
