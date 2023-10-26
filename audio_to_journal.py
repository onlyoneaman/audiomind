import time

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

from prompts import PROMPT_TEMPLATES

from util import load_config, person_info, store_results, get_args, get_env_var, get_main_file_name
from helpers.audio_utils import transcribe_and_store
from helpers.llm_util import get_text_splitter, initialize_llm


def transcribe_file(audio_file):
    start_time = time.time()
    print("Started transcribing...")
    transcript = transcribe_and_store(audio_file)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Transcribing Done. Time taken: {elapsed_time:.2f} seconds")
    return transcript


def make_docs(plain_text: str) -> list:
    texts = get_text_splitter().split_text(plain_text)
    docs = [Document(page_content=t) for t in texts]
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


def summarize_doc(llm, transcript, person_details):
    # Start the timer
    start_time = time.time()

    print("Started summarizing...")
    local_start_time = time.time()
    summary_prompt_template = PROMPT_TEMPLATES["notes_template"]    
    summary = summarize(llm, transcript, person_details, summary_prompt_template)

    elapsed_time = time.time() - local_start_time
    print(f"Generated Summary. Time taken: {elapsed_time:.2f}s")
    print(summary)

    local_start_time = time.time()
    title_prompt_template = PROMPT_TEMPLATES["title_description_template"]
    title_description = summarize(llm, summary, person_details, title_prompt_template, chain_type="map_reduce", variables=["text"])

    elapsed_time = time.time() - local_start_time
    print(f"Generated Title. Time taken: {elapsed_time:.2f}s")
    print("Title, description: ", title_description)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Summarizing Done. Time taken: {elapsed_time:.2f} seconds")
    return {
        "title_description": title_description,
        "summary": summary,
    }


def check():
    main_envs = ["AUDIO_FILE", "TRANSCRIPT_DIR", "WHISPER_MODEL", "OPENAI_MODEL", "RESULTS_DIR"]
    return [env for env in main_envs if get_env_var(env, check_exists=True) is None]


def main():
    try:
        load_config()
        get_args()
        check()
        start_time = time.time()
        main_file_name = get_env_var("AUDIO_FILE")
        audio_file = f"./{main_file_name}"
        main_base = get_main_file_name(main_file_name)

        print("Started processing...")
        llm = initialize_llm()
        details = person_info()

        transcript = transcribe_file(audio_file)

        results = summarize_doc(llm, transcript, details)
        title_description = results["title_description"]
        summary = results["summary"]

        result_filename = store_results(main_base, title_description, summary)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Done. Time taken: {elapsed_time:.2f} seconds")
        print("Check Results at: ", result_filename)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
