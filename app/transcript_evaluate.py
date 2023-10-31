import whisper
import os
import string
import subprocess
from typing import List

def read_bad_words() -> List[str]:
    """
    Read a list of bad words from a text file.

    Returns:
        List[str]: A list of bad words.
    """
    bad_words = []
    folder_path = os.getcwd()
    path_bad_words = os.path.join(folder_path, 'bad_words.txt')
    with open(path_bad_words, 'r') as file:
        for line in file:
            bad_words.append(line.strip())
    return bad_words

def init_model(size='tiny'):
    """
    Initialize a Whisper ASR model.

    Args:
        size (str, optional): Model size. Defaults to 'tiny'.

    Returns:
        Model: A Whisper ASR model.
    """
    model = whisper.load_model(size)
    return model

def transcript(audio_wav_path: str, model):
    """
    Transcribe an audio WAV file using the provided Whisper model.

    Args:
        audio_wav_path (str): Path to the audio WAV file.
        model: The Whisper ASR model.

    Returns:
        str: Transcribed text from the audio.
    """
    transcription = model.transcribe(audio_wav_path)
    return transcription["text"]

def evaluate(text: str, bad_words: List[str]):
    """
    Evaluate text for the presence of bad words and its overall sentiment.

    Args:
        text (str): Text to evaluate.
        bad_words (List[str]): A list of bad words.

    Returns:
        str: Text with evaluation including POS/NEG and the number of bad words.
    """
    text_to_analyze = str(text)
    translator = str.maketrans('', '', string.punctuation)
    text_to_analyze = text_to_analyze.translate(translator)

    words_in_text = text_to_analyze.split()

    bad_word_in_text = []
    for word in bad_words:
        if word in words_in_text:
            bad_word_in_text.append(word)

    number_bad_words = len(bad_word_in_text)
    if len(bad_word_in_text) == 0:
        evaluation = 'Positive'
    else:
        evaluation = 'Negative'
    final_text = f'Evaluation: {evaluation} \nNumber of bad words: {number_bad_words} \n' + text

    return final_text

def transcript_and_evaluate(input_audio_path: str, bad_words: List[str], model):
    """
    Transcribe and evaluate an audio file.

    Args:
        input_audio_path (str): Path to the input audio file (MP3).
        bad_words (List[str]): A list of bad words.
        model: The Whisper ASR model.

    Returns:
        str: Evaluated transcription result.
    """
    # Convert MP3 to WAV
    audio_wav_path = input_audio_path.replace('.mp3', '.wav')
    subprocess.run(["ffmpeg", "-i", input_audio_path, audio_wav_path])

    # Transcribe and evaluate
    transcription = transcript(audio_wav_path, model=model)
    evaluated_transcription = evaluate(text=transcription, bad_words=bad_words)

    # Clean up working directory
    os.remove(audio_wav_path)

    return evaluated_transcription
