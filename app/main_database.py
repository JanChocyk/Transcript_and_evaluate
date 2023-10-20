# docelowo potrzebuję wywoływać funkcję transcript_and_evaluate() i przekazywać do niej mp3, bad_words i model
# ALGORYTM:
# 1. Pobrać z bazy danych plik MP3
# 2. Zapisać go jako MP3 do folderu input
# 3. przekazać tę ścieżkę do funkcji
# 4. zapisać transkrypcję do bazy danych

# TABELA Nagrania:
# CREATE TABLE Nagrania (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     plikMP3 LONGBLOB,
#     transkrypcje TEXT
# );

# W których momentach mogą pojawić się błędy?

from db_config import MySQLConnector
from transcript_evaluate import transcript_and_evaluate, read_bad_words, init_model

import os

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD_TO_DB')
DATABASE = 'nagrania'


def save_mp3(mp3_binary_data, id):
    mp3_file_name = f'{id}_file.mp3'
    mp3_file_path = os.path.join(".\\work_director", mp3_file_name)
    with open(mp3_file_path, "wb") as mp3_file:
        mp3_file.write(mp3_binary_data)
    return mp3_file_path


def main():
    model_to_transcript = init_model()
    bad_words = read_bad_words()

    try:
        db = MySQLConnector(HOST, USER, PASSWORD, DATABASE)
        ids_to_work = db.select_id()
        for id, *_ in ids_to_work:
                mp3_binary_data = db.select_mp3(id)
                try:
                    input_audio_path = save_mp3(mp3_binary_data, id)
                    evaluated_transcription = transcript_and_evaluate(input_audio_path=input_audio_path, bad_words=bad_words, model=model_to_transcript)
                    db.save_new_transcription(evaluated_transcription, id)
                    os.remove(input_audio_path)
                except:
                    print(f"Wystąpił błąd podczas przetwarzania rekordu {id}.")
        db.connection.close()
    except:
        print('Nie udało się nawiązać połączenia z bazą danych. Program kończy swoje działanie.')


if __name__ == "__main__":
    main()
