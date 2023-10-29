# AudioMind

## Overview

AudioMind is a Python-based solution designed to extract meaningful insights from audio files. By leveraging whisper and LLMs, the platform transcribes and summarizes audio content, making it easier to derive actionable information.

### Stack

#### LLM
   - OpenAI

#### Speech to Text
   - Whisper (Openai API) [DEFAULT]
   - Whisper (On-Device)

### Current Solutions

- Create a journal entry from your voice note.

## Goals

- Transcribe audio files to text.
- Summarize the transcribed text.
- Easy to integrate and use.
- Get Insights from any audio file, including podcasts , interviews, lectures, etc.
- Solve actual problems.

## Installation

### Prerequisites

- Python 3.x
- pip

### Use [PIP](https://pypi.org/project/audiomind/0.2.0/) Package (Recommended)

```bash
pip install audiomind
```

```python
from audiomind import AudioMind

audiomind = AudioMind()
audiomind.process(file="examples/1.mp3")
```


### Steps to Install

1. **Clone the Repository**

    ```bash
    git clone https://github.com/onlyoneaman/audiomind.git
    cd audiomind
    ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv .venv
    ```

    Activate the virtual environment:

    - **Unix or MacOS**

        ```bash
        source .venv/bin/activate
        ```
    
    - **Windows**

        ```bash
        .\.venv\Scripts\activate
        ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Variables**

    Copy `.env.template` to `.env`.

    ```bash
    cp .env.template .env
    ```

    Open `.env` and provide your OpenAI API key:

    ```dotenv
    OPENAI_API_KEY=your_openai_api_key_here
    DREAMBOAT_API_KEY=your_dreamboat_api_key_here // optional
    ```

5. **Run the Application**

    ```bash
    python3 -m audiomind
    ```

## Usage

Place the audio files in the `/exmaples` folder and run the `audio_to_journal.py` script. The script will transcribe the audio and summarize it.

```bash
python3 -m audiomind --file examples/1.mp3
```

You can add some information about yourself in `person.txt` file.
Audiomind will use this information too while creating the journal entry.

### Roadmap

- [x] Transcribe audio files to text.
- [x] Summarize the transcribed text.
- [x] Easy to integrate and use.
- [x] Get Insights from any audio file, including podcasts , interviews, lectures, etc.
- [X] Create a journal entry from your voice note.
- [ ] Improve the journal entry.
- [ ] Create a summary of a podcast episode.
- [ ] Create a summary of a lecture.
- [ ] Create a summary of a meeting.

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT

---

Enjoy using AudioMind!