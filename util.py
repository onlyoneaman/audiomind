import openai
from dotenv import load_dotenv
import os
import time
import argparse
import yaml


def get_env_var(var_name, check_exists=False):
    """Fetch and validate an environment variable"""
    var_value = os.getenv(var_name)
    if check_exists and not var_value:
        raise EnvironmentError(f"{var_name} is not set")
    if var_value is None and check_exists:
        raise EnvironmentError(f"{var_name} is not set")
    return var_value


def person_info(person_file=None):
    try:
        if person_file is None:
            person_file = get_env_var("USER_FILE")
        if not os.path.exists(person_file):
            print("Error: Person file does not exist.")
            return None
        with open(person_file, "r") as f:
            return f.read()
    except Exception as e:
        print("Error: ", e)
        return None


def store_results(basename, title_description, summary):
    results_folder = get_env_var("RESULTS_DIR")
    os.makedirs(results_folder, exist_ok=True)
    filename = f"{results_folder}/{int(time.time())}_{basename}.md"
    with open(filename, "w") as f:
        f.write(f"{title_description}\n\n{summary}\n")
    return filename


def get_main_file_name(audio_file):
    main_file = os.path.splitext(os.path.basename(audio_file))[0]
    return main_file


def get_args():
    parser = argparse.ArgumentParser(description='Process some flags for the script.')
    parser.add_argument('--file', help='The main file name to process')
    parser.add_argument('--transcript_dir', help='The directory where transcripts will be saved')
    parser.add_argument('--whisper_model', help='The whisper model to use')
    parser.add_argument('--openai_model', help='The AI model to use')
    parser.add_argument('--force_transcript', help='Force transcript generation')
    parser.add_argument('--whisper_api', help='Use the whisper API')
    args = parser.parse_args()
    if args.file is not None:
        os.environ["AUDIO_FILE"] = args.file
    if args.transcript_dir is not None:
        os.environ["TRANSCRIPT_DIR"] = args.transcript_dir
    if args.whisper_model is not None:
        os.environ["WHISPER_MODEL"] = args.whisper_model
    if args.openai_model is not None:
        os.environ["OPENAI_MODEL"] = args.openai_model
    if args.force_transcript is not None:
        os.environ["FORCE_TRANSCRIPT"] = args.force_transcript
    if args.whisper_api is not None:
        os.environ["USE_WHISPER_API"] = args.whisper_api
    return args


def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def load_config():
    load_dotenv()
    openai.api_key = get_env_var("OPENAI_API_KEY")
    try:
        config = load_yaml_config('./helpers/config.yaml')
        for key, value in config.items():
            os.environ.setdefault(key, value)
    except Exception as e:
        print(e)
        print("Error loading config file.")
