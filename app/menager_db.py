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
    """
    Add an MP3 file to a MySQL database.

    Args:
        mp3_file_path (str): Path to the MP3 file to be added.

    Returns:
        None
    """
    try:
        # Open the MP3 file and read it as binary data
        with open(mp3_file_path, 'rb') as mp3_file:
            mp3_binary_data = mp3_file.read()

        # Connect to the database
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # Create a cursor for executing SQL commands
        cursor = db.cursor()

        # Insert the MP3 file into the Nagrania table
        query = "INSERT INTO Nagrania (plikMP3) VALUES (%s);"
        data = (mp3_binary_data,)
        cursor.execute(query, data)

        # Commit changes to the database
        db.commit()

        # Close the database connection
        db.close()

        print("MP3 file added to the database successfully.")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    add_mp3_to_database()
