# Project: Telemarketer Recording Transcription and Evaluation Application

## Brief Project Description
This application is designed for a call center company that stores MP3 recordings of calls in a database. The application's main goal is to transcribe and evaluate each call, then save the results in the database. The application can be deployed in two ways:
- **A program running on the database server** (main_database.py), which automatically transcribes and evaluates calls every evening.
- **A REST API** that allows sending audio file URLs for transcription and evaluation.

The project utilizes the Whisper model by OpenAI for transcription.

## Technologes
- Python
- Flask
- MySQL

## Installation
You can download the project from [GitHub](https://github.com/JanChocyk/Transcript_and_evaluate.git).

## Usage
How you use the project depends on the chosen platform:

### Program running on the database server
- Run the `main_database.py` file on a server with database access.
  
### REST API
- Deploy the project on a publicly accessible server.
- Send POST requests with audio file URLs to the `/transcribe_and_evaluate` endpoint.
- Receive transcription and evaluation results in JSON format.

## Project Status
The project is actively under development.

## Author
Jan Chocyk

Project based on technologies: Python, Flask, MySQL.

For assistance or feedback, please contact: jan.chocyk@example.com
