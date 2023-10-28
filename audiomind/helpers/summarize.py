import time

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

from audiomind.prompts import PROMPT_TEMPLATES

from audiomind.helpers.llm_util import get_text_splitter


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


def summarize_text(
        llm, message: str, person_details: str, prompt_template: str,
        chain_type: str = "stuff", variables: list = ["text", "details"]
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
