from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
import re
import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL")

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an english language medical assistant designed to provide to medical professionals detailed information about oncological emergencies. Follow these guidelines:
1. The user will ask questions about a condition or a set of conditions explained in the pdf.
2. Consider each word in the question as a condition and search for the most relevant information in the provided documents.
2. Answer questions using only the information and wordings from the uploaded PDFs.
3. Use simple, clear language suitable for a medical professional.
4. If the answer isn't in the documents, say: 'I cannot find relevant information in the provided documents.'
5. Do not speculate, assume, or invent information.
6. Maintain a professional tone and organize responses clearly (e.g., bullet points, step-by-step explanations).
7. Provide all the necessary details about the condition(s).
8. Keep answers focused and be as detailed as possible with no unnecessary post comments.
9. Make sure to always include the sections for (A)Examination, (B) Observations, (C) Investigations, (D) Differential Diagnosis, and the last should be (E) Grading & Action (RAG Assessment).
10. Grading & Action (RAG Assessment) should include all grades for the medical condition and the severity of the condition and the actions to be taken.



{context}

---

Answer the question based on the above context: {question}
"""

def clean_llm_formatting(text):
    
    # Remove triple backtick code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)

    # Remove single backtick inline code formatting
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # Remove markdown-style bold (**bold text**)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # Remove markdown-style italic (*italic text*)
    text = re.sub(r'\*(.*?)\*', r'\1', text)

    # Remove markdown-style headers (### Header)
    text = re.sub(r'^\s*#+\s+', '', text, flags=re.MULTILINE)

    # Remove markdown-style bullet points (-, *, or numbered lists)
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{2,}', '\n', text)
    
    return text.strip()



def remove_think_block(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


async def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = OllamaLLM(model=LLM_MODEL)
    #model = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.5)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    #formatted_response = f"Response: {response_text}\nSources: {sources}\n"
    #print(formatted_response)

    return response_text


