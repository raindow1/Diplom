from Database.ClickhouseDB import ClickhouseDB
from deep_translator import GoogleTranslator
import time
from Translation.PatentTranslator import PatentTranslator

def create_chunks(corpus, max_chunk_size):
    chunks = [corpus[i:i + max_chunk_size] for i in range(0, len(corpus), max_chunk_size)]
    return chunks


def translate(field, max_chunk_size):
    if len(field) > max_chunk_size:
        results_list = []
        concatenated_result = ""

        original_chunks = create_chunks(field, max_chunk_size)
        for i in original_chunks:
            r = GoogleTranslator(source='en', target='ru').translate(text=i)
            time.sleep(10)
            results_list.append(r)

        for i in results_list:
            concatenated_result += i

        return concatenated_result
    else:
        res = GoogleTranslator(source='en', target='ru').translate(text=field)
        time.sleep(10)
        return res


def translate_text(Id):


    max_chunk_size = 4000
    trans = PatentTranslator()
    db_client = ClickhouseDB()
    index = db_client.select_from_db(db_client.database, db_client.db_ipc_patents, ["Index"], Id).result_rows[0][0]
    result = db_client.select_from_db(db_client.database, db_client.db_ipc_patents, ["Description", "Abstract"], Id)
    solution = db_client.select_from_db(db_client.database, db_client.db_ipc_patents, ["Title"], Id).result_rows[0][0]
    description = result.result_rows[0][0]
    abstract = result.result_rows[0][1]
    if 'RU' not in index:
        translated_solution = trans.translate_text(solution, max_chunk_size)
        #print(translated_solution)
        translated_description = translate(description, max_chunk_size)
        #print(translated_description)
        #translated_abstract = translate(abstract, max_chunk_size)
        #print(translated_abstract)


    return translated_description


def main():
    print(translate_text(4))


if __name__ == "__main__":
    main()
