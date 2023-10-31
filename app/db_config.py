# TABEL Nagrania:
# CREATE TABLE Nagrania (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     plikMP3 LONGBLOB,
#     transkrypcje TEXT
# );

import mysql.connector

class MySQLConnector:
    """
    A class for connecting to a MySQL database and performing various operations.
    
    Attributes:
        connection: A MySQL database connection.
        mycursor: A cursor for executing SQL queries.
    """
    
    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Initializes a new MySQLConnector object.

        Args:
            host (str): The hostname of the MySQL server.
            user (str): The MySQL user to authenticate.
            password (str): The password for the MySQL user.
            database (str): The name of the MySQL database.
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.mycursor = self.connection.cursor()

    def select_id(self) -> list[int]:
        """
        Selects IDs of records with NULL transcriptions.

        Returns:
            list[int]: A list of IDs.
        """
        query = "SELECT id FROM Nagrania WHERE transkrypcje IS NULL;"
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def select_mp3(self, id: int) -> bytes:
        """
        Selects the binary representation of an MP3 file by ID.

        Args:
            id (int): The ID of the record.

        Returns:
            bytes: The binary representation of the MP3 file.
        """
        query = "SELECT plikMP3 FROM Nagrania WHERE id = %s;"
        self.mycursor.execute(query, [id])
        result = self.mycursor.fetchall()
        mp3_binary, *_ = result[0]
        return mp3_binary

    def save_new_transcription(self, evaluated_transcription: str, id: int):
        """
        Saves a new transcription for a record.

        Args:
            evaluated_transcription (str): The evaluated transcription.
            id (int): The ID of the record.
        """
        query = "UPDATE Nagrania SET transkrypcje = %s WHERE id = %s;"
        self.mycursor.execute(query, (evaluated_transcription, id))
        self.connection.commit()

    def add_new_record(self, mp3_path: str, transcript_and_evaluate: str):
        """
        Adds a new record to the database.

        Args:
            mp3_path (str): The path to the MP3 file.
            transcript_and_evaluate (str): The evaluated transcription.
        """
        binary_representation = make_binary_format(mp3_path)
        # Insert the MP3 file into the Nagrania table
        query = "INSERT INTO Nagrania (plikMP3, transkrypcje) VALUES (%s, %s);"
        self.mycursor.execute(query, [binary_representation, transcript_and_evaluate])

def make_binary_format(mp3_path: str) -> bytes:
    """
    Converts an MP3 file to binary format.

    Args:
        mp3_path (str): The path to the MP3 file.

    Returns:
        bytes: The binary representation of the MP3 file.
    """
    with open(mp3_path, 'rb') as mp3_file:
        mp3_binary_data = mp3_file.read()
    return mp3_binary_data
