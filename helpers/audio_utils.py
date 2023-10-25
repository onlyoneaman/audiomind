import os
import errno
import whisper

from util import get_env_var


def transcribe_and_store(audio_file, transcript_file, transcript_folder):
    if transcript_folder is None:
        transcript_folder = get_env_var("TRANSCRIPT_DIR")
    transcript = transcribe(audio_file, transcript_file)
    os.makedirs(transcript_folder, exist_ok=True)
    with open(transcript_file, "w") as f:
        f.write(transcript)
    return transcript


def transcribe(audio_file, transcript_file):
    if os.path.exists(transcript_file):
        with open(transcript_file, "r") as f:
            transcript = f.read()
            if len(transcript) > 0:
                print("Transcript found.")
                return transcript
    if not os.path.exists(audio_file):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), audio_file)
    whisper_model = get_env_var("WHISPER_MODEL")
    model = whisper.load_model(whisper_model, in_memory=True)
    return model.transcribe(audio_file, verbose=False)["text"]
