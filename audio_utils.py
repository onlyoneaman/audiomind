import os
import errno
import whisper

def transcribe(audio_file, transcript_file):
    if os.path.exists(transcript_file):
        with open(transcript_file, "r") as f:
            transcript = f.read()
            if len(transcript) > 0:
                return transcript
    if not os.path.exists(audio_file):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), audio_file)
    model = whisper.load_model("base", in_memory=True)
    return model.transcribe(audio_file, verbose=False)["text"]
