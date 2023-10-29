from dotenv import load_dotenv
import openai
import os
import argparse
import yaml
import pkg_resources


def get_env_var(var_name, check_exists=False):
    """Fetch and validate an environment variable"""
    var_value = os.getenv(var_name)
    if check_exists and not var_value:
        raise EnvironmentError(f"{var_name} is not set")
    if var_value is None and check_exists:
        raise EnvironmentError(f"{var_name} is not set")
    return var_value


def get_default_audio_file():
    return pkg_resources.resource_filename(__name__, get_env_var("AUDIO_FILE"))


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


def get_args():
    parser = argparse.ArgumentParser(description='Process some flags for the script.')
    parser.add_argument('--file', help='The main file name to process')
    parser.add_argument('--transcript_dir', help='The directory where transcripts will be saved')
    parser.add_argument('--whisper_model', help='The whisper model to use')
    parser.add_argument('--openai_model', help='The AI model to use')
    parser.add_argument('--force_transcript', help='Force transcript generation')
    parser.add_argument('--whisper_api', help='Use the whisper API')
    args = parser.parse_args()
    return args


def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def load_config():
    load_dotenv()
    setup_openai()
    try:
        config_path = pkg_resources.resource_filename(__name__, 'helpers/config.yaml')
        config = load_yaml_config(config_path)
        for key, value in config.items():
            os.environ.setdefault(key, value)
    except Exception as e:
        print(e)
        print("Error loading config file.")


def setup_openai():
    openai.api_key = get_env_var("OPENAI_API_KEY")


def check():
    main_envs = ["AUDIO_FILE", "TRANSCRIPT_DIR", "WHISPER_MODEL", "OPENAI_MODEL", "RESULTS_DIR"]
    return [env for env in main_envs if get_env_var(env, check_exists=True) is None]
