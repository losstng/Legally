from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.services.vector_store import retrieve_relevant_chunks 
import os
from app.utils.language import detect_language, SUPPORTED_LANGUAGES
from dotenv import load_dotenv
load_dotenv()

#from services.embedding_loader import load_and_chunk
#from services.vector_store import store_chunks_in_vector_db

#chunks = load_and_chunk("data/asylum_law.pdf")
#store_chunks_in_vector_db(chunks)

openai_model = ChatOpenAI(
    temperature=0.2,
    model=os.getenv("LLM_MODEL")) # this is just to get the base answer

def get_system_prompt(lang: str, context: str) -> str: # base answer for system prompt # base answer
    if lang == "de":
        return f"""
Du bist ein juristischer Assistent, der Fragen zum Asylrecht beantwortet.
Nutze ausschließlich den folgenden KONTEXT für deine Antwort.
Wenn der KONTEXT unzureichend ist, sage: "Auf Basis der gegebenen Informationen kann keine endgültige Antwort gegeben werden."

KONTEXT:
{context}
"""
    elif lang == "vi":
        return f"""
Bạn là trợ lý pháp lý chuyên giải đáp các câu hỏi liên quan đến luật nhập cư và tị nạn.
Chỉ sử dụng bối cảnh sau đây để trả lời. Không sử dụng kiến thức bên ngoài.

Nếu bối cảnh không đầy đủ, hãy nói: "Dựa trên thông tin đã cho, không thể đưa ra câu trả lời chính xác."

BỐI CẢNH:
{context}
"""
    else:  # Default: English
        return f"""
You are a legal assistant answering questions regarding laws.
Use the following legal CONTEXT when crafting your response.
Only use the provided CONTEXT below to answer. Do not rely on prior knowledge.

If CONTEXT is missing or insufficient, say: "Based on the given information, a definitive answer cannot be provided."

CONTEXT:
{context}
"""
def ask_legal_question_with_context(question: str, context: str, lang: str = "en") -> str: # we have a default in case the lang is wrong
    system_prompt=get_system_prompt(lang, context)
    
    messages = [
        SystemMessage(content=system_prompt.strip()), # foreground for the main play
        HumanMessage(content=question)    # the main play
    ]
    return openai_model.invoke(messages).content # get the core the message, and the content of it, ESSENTIALY so

def get_limited_context(question: str, max_tokens=1500):
    chunks = retrieve_relevant_chunks(question, k=10) # get that chunks using similarity search, the top 10
    context = "" #will be appended in this
    total_tokens = 0

    for chunk in chunks:
        token_count = len(chunk.split()) # split it accordingly to maximize, hit it first before we have to do it
        if total_tokens + token_count > max_tokens:
            break
        context += chunk + "\n\n"
        total_tokens += token_count # it has to be equal to this one

        # crazy discrete math in this one

    return context
