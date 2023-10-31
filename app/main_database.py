from db_config import MySQLConnector
from transcript_evaluate import transcript_and_evaluate, read_bad_words, init_model

import os

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD_TO_DB')
DATABASE = 'nagrania'

def save_mp3(mp3_binary_data: bytes, id: int) -> str:
    """
    Save MP3 binary data to a file.

    Args:
        mp3_binary_data (bytes): The binary data of the MP3 file.
        id (int): The ID associated with the MP3 file.

    Returns:
        str: The file path where the MP3 file is saved.
    """
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
                print(f"An error occurred while processing record {id}.")
        db.connection.close()
    except:
        print('Failed to establish a connection to the database. The program is exiting.')

if __name__ == "__main__":
    main()
