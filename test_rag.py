from query_data import query_rag
from langchain_community.llms.ollama import Ollama
import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL")

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def query_and_validate(question, expected_response):
    actual_response = query_rag(question)
    eval_prompt = EVAL_PROMPT.format(expected_response=expected_response, actual_response=actual_response)
    llm = Ollama(model=LLM_MODEL)
    evaluation = llm(eval_prompt)
    return evaluation.strip().lower() == 'true'

def test_bowel_min_days():
    assert query_and_validate(
        question="For people with no bowel movement for 24 hours, should we consider the use of laxatives?",
        expected_response="True",
    )

def test_extravasation():
    assert query_and_validate(
        question="Extravasation is the accidental administration of drugs into the heart?",
        expected_response="False",
    )

def test_bowel_min_days():
    assert query_and_validate(
        question="For people with no bowel movement for 24 hours, should we consider the use of laxatives?",
        expected_response="True",
    )

def test_extravasation():
    assert query_and_validate(
        question="Extravasation is the accidental administration of drugs into the heart?",
        expected_response="False",
    )

def test_hypertension_treatment():
    assert query_and_validate(
        question="Is lifestyle modification the first line of treatment for hypertension?",
        expected_response="True",
    )

def test_diabetes_insulin():
    assert query_and_validate(
        question="Is insulin the only treatment for type 1 diabetes?",
        expected_response="True",
    )

def test_vitamin_c_deficiency():
    assert query_and_validate(
        question="Can vitamin C deficiency lead to scurvy?",
        expected_response="True",
    )
