from dotenv import load_dotenv
import os
import time
import argparse

from audio_utils import transcribe

load_dotenv()

DEFAULT_AUDIO = "How-will-AI-change-the-world.mp3"
DEFAULT_AUDIO_DIR = "examples"
DEFAULT_TRANSCRIPT_DIR = "transcripts"

def get_env_var(var_name):
    """Fetch and validate an environment variable"""
    var_value = os.getenv(var_name)
    if var_value is None:
        raise EnvironmentError(f"{var_name} is not set")
    return var_value

def person_info(person_file="person.txt"):
    if not os.path.exists(person_file):
        print("Error: Person file does not exist.")
        return None
    with open(person_file, "r") as f:
        return f.read()

def store_results(basename, title_description, summary, results_folder="results"):
    os.makedirs(results_folder, exist_ok=True)
    filename = f"{results_folder}/{int(time.time())}_{basename}.md"
    with open(filename, "w") as f:
        f.write(f"{title_description}\n\n{summary}\n")

def transcribe_and_store(audio_file, transcript_file, transcript_folder=DEFAULT_TRANSCRIPT_DIR):
    transcript = transcribe(audio_file, transcript_file)
    os.makedirs(transcript_folder, exist_ok=True)
    with open(transcript_file, "w") as f:
        f.write(transcript)
    return transcript

def get_args():
    parser = argparse.ArgumentParser(description='Process some flags for the script.')
    parser.add_argument('--main_file_name', default=DEFAULT_AUDIO, help='The main file name to process')
    parser.add_argument('--audio_dir', default=DEFAULT_AUDIO_DIR, help='The directory where audio files are stored')
    parser.add_argument('--transcript_dir', default=DEFAULT_TRANSCRIPT_DIR, help='The directory where transcripts will be saved')
    args = parser.parse_args()
    return args