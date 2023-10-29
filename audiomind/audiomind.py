import time
import os
from typing import Optional

from audiomind.prompts import PROMPT_TEMPLATES

from audiomind.util import get_args, load_config, check, person_info, get_env_var, get_default_audio_file
from audiomind.helpers.llm_util import initialize_llm
from audiomind.helpers.audio_utils import transcribe_and_store
from audiomind.helpers.summarize import summarize_text


class AudioMind:

    def __init__(self,
                 file: Optional[str] = None,
                 transcript_dir: Optional[str] = None,
                 whisper_model: Optional[str] = None,
                 openai_model: Optional[str] = None,
                 force_transcript: Optional[bool] = None,
                 whisper_api: Optional[bool] = None):
        """
            Initializes the AudioMind object.
            :param file: Path to the audio file.
            :param transcript_dir: Directory for transcripts.
            :param whisper_model: Whisper model for transcription.
            :param openai_model: OpenAI model for summarization.
            :param force_transcript: Flag to force transcription.
            :param whisper_api: Flag to use Whisper API.
        """
        self.load_configuration()
        args = get_args()
        self.file = file or args.file or get_default_audio_file()
        self.transcript_dir = self.set_env_if_value("TRANSCRIPT_DIR", transcript_dir or args.transcript_dir)
        self.whisper_model = self.set_env_if_value("WHISPER_MODEL", whisper_model or args.whisper_model)
        self.openai_model = self.set_env_if_value("OPENAI_MODEL", openai_model or args.openai_model)
        self.force_transcript = self.set_env_if_value("FORCE_TRANSCRIPT", force_transcript or args.force_transcript)
        self.whisper_api = self.set_env_if_value("USE_WHISPER_API", whisper_api or args.whisper_api)
        check()
        self.audio_file = None
        self.base_name = None
        self.llm = None
        self.person_details = None
        self.transcript = None
        self.summary = None
        self.title_description = None
        self.setup()


    @classmethod
    def set_env_if_value(cls, env_var, value):
        if value is not None:
            os.environ[env_var] = value
        else:
            value = get_env_var(env_var)
        return value

    def load_configuration(self):
        """
        Loads configurations for AudioMind.
        """
        load_config()

    @staticmethod
    def get_main_file_name(file_name):
        main_file = os.path.splitext(os.path.basename(file_name))[0]
        return main_file

    def setup(self):
        self.llm = initialize_llm()
        self.person_details = person_info()
        self.audio_file = self.file
        self.base_name = self.get_main_file_name(self.file)

    def process(self):
        print('Starting...')
        try:
            start_time = time.time()
            self.transcribe()
            self.summarize()
            result_filename = self.save_results()
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"Done in {elapsed:.2f} secs")
            print(f"Wrote results to {result_filename}")
        except Exception as e:
            print("Error:", e)

    def transcribe(self):
        start_time = time.time()
        print("Started transcribing...")
        self.transcript = transcribe_and_store(self.audio_file, self.base_name)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Transcribing Done. Time taken: {elapsed_time:.2f} seconds")

    def summarize(self):
        start_time = time.time()
        print("Started summarizing...")
        local_start_time = time.time()
        summary_prompt_template = PROMPT_TEMPLATES["notes_template"]
        self.summary = summarize_text(self.llm, self.transcript, self.person_details, summary_prompt_template)

        elapsed_time = time.time() - local_start_time
        print(f"Generated Summary. Time taken: {elapsed_time:.2f}s")

        local_start_time = time.time()
        title_prompt_template = PROMPT_TEMPLATES["title_description_template"]
        self.title_description = summarize_text(self.llm, self.summary, self.person_details, title_prompt_template,
                                           chain_type="map_reduce",variables=["text"])

        elapsed_time = time.time() - local_start_time
        print(f"Generated Title. Time taken: {elapsed_time:.2f}s")

        final_elapsed_time = time.time() - start_time
        print(f"Summarizing Done. Time taken: {final_elapsed_time:.2f} seconds")

    def save_results(self):
        results_folder = get_env_var("RESULTS_DIR")
        os.makedirs(results_folder, exist_ok=True)
        filename = f"{results_folder}/{int(time.time())}_{self.base_name}.md"
        with open(filename, "w") as f:
            f.write(f"{self.title_description}\n\n{self.summary}\n")
        return filename
