# TABELA Nagrania:
# CREATE TABLE Nagrania (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     plikMP3 LONGBLOB,
#     transkrypcje TEXT
# );

import mysql.connector


class MySQLConnector():
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        self.mycursor = self.connection.cursor()

    def select_id(self):
        query = "SELECT id FROM Nagrania WHERE transkrypcje IS NULL;"
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
    
    def select_mp3(self, id: int):
        query = "SELECT plikMP3 FROM Nagrania WHERE id = %s;"
        self.mycursor.execute(query, [id])
        result = self.mycursor.fetchall()
        mp3_binary, *_ = result[0]
        return mp3_binary

    def save_new_transcription(self, evaluated_transcription: str, id: int):
        query = "UPDATE Nagrania SET transkrypcje = %s WHERE id = %s;"
        self.mycursor.execute(query, (evaluated_transcription, id))
        self.connection.commit()

