from flask import Flask, request, jsonify
import os
import requests
from transcript_evaluate import transcript_and_evaluate, read_bad_words, init_model
import db_config

app = Flask(__name__)
model = init_model()
bad_words = read_bad_words()
mp3_path = os.path.join(os.getcwd(), 'work_directory', 'audio.mp3')


@app.route('/transcribe_and_evaluate', methods=['POST'])
def transcribe_audio() -> jsonify:
    """
    REST API endpoint for audio transcription and evaluation.

    Receives the audio file's URL, downloads it, transcribes and evaluates it, stores the result in a database,
    and returns the result in JSON format.

    Returns:
        JSON: Transcription and evaluation result.

    Raises:
        400 Bad Request: In case of missing audio file URL or an error during file download.
        500 Internal Server Error: In case of other errors.

    """
    try:
        data = request.get_json()
        audio_url = data.get('audio_url')

        if not audio_url:
            return jsonify({"error": "Missing audio file URL"}), 400

        # Download the MP3 file from the provided URL
        response = requests.get(audio_url)
        if response.status_code != 200:
            return jsonify({"error": "Unable to download the audio file from the provided URL"}), 400

        # Save the file in the working directory
        with open(mp3_path, "wb") as audio_file:
            audio_file.write(response.content)

        # Call the transcript_and_evaluate function on the saved file
        result = transcript_and_evaluate(mp3_path, bad_words, model)
        db = db_config.MySQLConnector()
        db.add_new_record(mp3_path, result)
        db.connection.close()

        # Remove the temporary file
        os.remove(mp3_path)

        # Return the result in JSON format
        return jsonify({"transcription_result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()

