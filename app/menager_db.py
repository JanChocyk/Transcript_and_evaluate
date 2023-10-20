import mysql.connector
import os
import click

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD_TO_DB')
DATABASE = 'nagrania'

@click.command()
@click.argument('mp3_file_path', type=click.Path(exists=True))
def add_mp3_to_database(mp3_file_path):
    try:
        # Otwórz plik MP3 i odczytaj go jako dane binarne
        with open(mp3_file_path, 'rb') as mp3_file:
            mp3_binary_data = mp3_file.read()

        # Połącz się z bazą danych
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # Utwórz kursor do wykonywania poleceń SQL
        cursor = db.cursor()

        # Wstaw plik MP3 do tabeli Nagrania
        query = "INSERT INTO Nagrania (plikMP3) VALUES (%s);"
        data = (mp3_binary_data,)
        cursor.execute(query, data)

        # Zatwierdź zmiany w bazie danych
        db.commit()

        # Zamknij połączenie z bazą danych
        db.close()

        print("Plik MP3 dodany do bazy danych pomyślnie.")

    except Exception as e:
        print("Wystąpił błąd:", str(e))

if __name__ == "__main__":
    add_mp3_to_database()
