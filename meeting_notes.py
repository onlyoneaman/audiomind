import time
import os
import whisper
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from prompts import PROMPT_TEMPLATES
import errno

def load_env_vars():
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_KEY is None:
        raise Exception("OPENAI_API_KEY is not set")

    USE_DREAMBOAT = False

    DREAMBOAT_KEY = os.getenv("DREAMBOAT_API_KEY")
    if DREAMBOAT_KEY is not None:
        USE_DREAMBOAT = True

    return OPENAI_KEY, USE_DREAMBOAT, DREAMBOAT_KEY

load_dotenv()

def initialize_model(OPENAI_KEY, USE_DREAMBOAT, DREAMBOAT_KEY):
    kwargs = {
        "temperature": 1,
        "model_name": "gpt-4",
        "openai_api_key": OPENAI_KEY
    }
    if USE_DREAMBOAT:
        kwargs.update({
            "openai_api_base": "https://dev.dreamboat.ai/v1/proxy",
            "headers": {
                "x-dreamboat-api-key": DREAMBOAT_KEY,
                "x-dreamboat-mode": "proxy openai"
            }
        })
    return ChatOpenAI(**kwargs)

# text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    # chunk_size=4000
# )
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=6500,
    chunk_overlap=20,
    length_function=len
)

# main_file_name = "winston-churchill-the-threat-of-germany.wav"
# audio_dir_name = "examples"
# main_file_name = "A short video for Understanding artificial intelligence.mp4"
main_file_name = "together fun meet.mp4"
audio_dir_name = "audios"
base_name = os.path.splitext(os.path.basename(main_file_name))[0]
transcript_file = f"./transcripts/{base_name}.txt"

def load_transcript(transcript_file):
    if not os.path.exists(transcript_file):
        print("Error: Transcript file does not exist.")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), transcript_file)
    docs = TextLoader(transcript_file)
    return docs.load()

def person_info():
    person_file = "person.txt"
    if not os.path.exists(person_file):
        print("Error: Person file does not exist.")
        return None
    with open(person_file, "r") as f:
        person = f.read()
    return person

def store_results(title_description, summary):
    results_folder = "results"
    try:
        os.makedirs(results_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    markdown_filename = f"{results_folder}/{int(time.time())}_{base_name}.md"
    with open(markdown_filename, "w") as f:
        f.write(f"{title_description}\n")
        f.write(f"{summary}\n")

def transcribe():
    start_time = time.time()

    print("Started transcribing...")

    if os.path.exists(transcript_file):
        with open(transcript_file, "r") as f:
            transcript = f.read()
            if len(transcript) > 0:
                return transcript

    audio_file = f"./{audio_dir_name}/{main_file_name}"
    if not os.path.exists(audio_file):
        print("Error: Audio file does not exist.")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), audio_file)

    model = whisper.load_model("base", in_memory=True)

    audio_file = f"./{audio_dir_name}/{main_file_name}"

    result = model.transcribe(audio_file, verbose=False)

    # Get the transcript
    transcript = result["text"]

    # Save the transcript to a text file
    with open(transcript_file, "w") as f:
        f.write(transcript)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Transcribing Done. Time taken: {elapsed_time:.2f} seconds")

    return transcript

def make_docs(plain_text: str) -> list:
    texts = text_splitter.split_text(plain_text)
    docs = [Document(page_content=t) for t in texts]
    print(len(docs))
    return docs

def summarize_docs(
    docs: list,
    prompt_template: str,
    details: str,
    model,
    variables: list,
    chain_type="stuff",
) -> str:
    prompt = PromptTemplate(template=prompt_template, input_variables=variables)

    if chain_type == "map_reduce":
        chain = load_summarize_chain(
            model, chain_type=chain_type, map_prompt=prompt, combine_prompt=prompt
        )
    else:
        chain = load_summarize_chain(model, chain_type=chain_type, prompt=prompt)
    values = {"input_documents": docs}
    if "details" in variables:
        values["details"] = details
    chain_output = chain(values, return_only_outputs=True)
    return chain_output["output_text"]

def summarize(
        llm, message: str, person_details: str,
        prompt_template: str, chain_type: str = "stuff",
        variables: list = ["text", "details"]
        ) -> str:
    docs = make_docs(message)
    summary_text = summarize_docs(
        docs,
        prompt_template,
        person_details,
        chain_type=chain_type,
        model=llm,
        variables=variables,
    )
    return summary_text

def summarize_doc(llm, transcript, person_info):
    # Start the timer
    start_time = time.time()

    print("Started summarizing...")
    local_start_time = time.time()
    summary_prompt_template = PROMPT_TEMPLATES["notes_template"]    
    summary = summarize(llm, transcript, person_info, summary_prompt_template, chain_type="map_reduce")

    elapsed_time = time.time() - local_start_time
    print(f"Generated Summary. Time taken: {elapsed_time:.2f}s")
    print(summary)

    local_start_time = time.time()
    title_prompt_template = PROMPT_TEMPLATES["title_description_template"]
    title_description = summarize(llm, summary, person_info, title_prompt_template, chain_type="map_reduce", variables=["text"])

    elapsed_time = time.time() - local_start_time
    print(f"Generated Title. Time taken: {elapsed_time:.2f}s")
    print("Title, description: ", title_description)

    store_results(title_description, summary)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Summarizing Done. Time taken: {elapsed_time:.2f} seconds")

def main():
    try:
        start_time = time.time()
        OPENAI_KEY, USE_DREAMBOAT, DREAMBOAT_KEY = load_env_vars()
        llm = initialize_model(OPENAI_KEY, USE_DREAMBOAT, DREAMBOAT_KEY)
        print("Started...")
        details = person_info() 
        transcript = transcribe()
        summarize_doc(llm, transcript, details)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Done. Time taken: {elapsed_time:.2f} seconds")
    except Exception as e:
        print(e.message)

if __name__ == "__main__":
    main()
