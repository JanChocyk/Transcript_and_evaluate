import whisper
import os
import string
import subprocess

def read_bad_words():
    bad_words = []
    # Otwieramy plik do odczytu (tryb 'r' oznacza odczyt)
    folder_path = os.getcwd()
    path_bad_words = os.path.join(folder_path, 'bad_words.txt')
    with open(path_bad_words, 'r') as plik:
        # Iterujemy przez linie pliku i dodajemy je do listy
        for linia in plik:
            bad_words.append(linia.strip())  # strip() usuwa białe znaki (np. znaki nowej linii)
    return bad_words


def init_model(size='tiny'):
    model = whisper.load_model(size)
    return model


def transcript(audio_wav_path, model):
    transcribtion = model.transcribe(audio_wav_path)
    return transcribtion["text"]


def evaluate(text: str, bad_words: list[str]):
    '''
    Funkcja ma zwracać tekst + dodana do niego ocena: POS/NEG i liczba "brzydkich słów"
    '''
    text_to_analyze = str(text)
    # Usuń interpunkcję z tekstu
    translator = str.maketrans('', '', string.punctuation)
    text_to_analyze = text_to_analyze.translate(translator)

    # Rozdziel tekst na słowa
    words_in_text = text_to_analyze.split()

    bad_word_in_text = []
    # Sprawdź, czy jakiekolwiek słowo z listy występuje w tekście
    for word in bad_words:
        if word in words_in_text:
            bad_word_in_text.append(word)

    # Jeśli nie znaleziono żadnego toksycznego słowa
    number_bad_words = len(bad_word_in_text)
    if len(bad_word_in_text) == 0:
        evaluate = 'Pozytywna'
    else:
        evaluate = 'Negatywna'
    final_text = f'Ocena: {evaluate} \nLiczba niedozwolonych słów: {number_bad_words} \n' + text

    return final_text


def transcript_and_evaluate(input_audio_path: str, bad_words: list[str], model):
    # zapisanie pliku jako WAV w work_directory
    audio_wav_path = input_audio_path.replace('.mp3', '.wav')
    subprocess.run(["ffmpeg", "-i", input_audio_path, audio_wav_path])

    # wywołanie funkcji transcript i przekazanie do niej patha pliku WAV i modelu 
    transcription = transcript(audio_wav_path, model=model)
    # wywołanie funkcji evaluate
    evaluated_transcription = evaluate(text=transcription, bad_words=bad_words)

    # wyczyszczenie katalogu roboczego
    os.remove(audio_wav_path)

    return evaluated_transcription
