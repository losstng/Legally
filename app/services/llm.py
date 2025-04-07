from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from services.vector_store import retrieve_relevant_chunks
import os
from dotenv import load_dotenv
load_dotenv()

#from services.embedding_loader import load_and_chunk
#from services.vector_store import store_chunks_in_vector_db

#chunks = load_and_chunk("data/asylum_law.pdf")
#store_chunks_in_vector_db(chunks)

openai_model = ChatOpenAI(
    temperature=0.2,
    model="",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
def ask_legal_question_with_context(question: str, context: str) -> str:
    system_prompt = f"""
    You are a legal assistant answering questions regarding laws.
Use the following legal context when crafting your response.
Only use the prvoided CONTEXT below to answer. Do not rely on prior knowledge.

If CONTEXT is missing or insufficient, say: "Based on the given information, a definitive answer cannot be provided."
Respond in a clear and concise tone suitable for legal advice.
Context:
{context}
"""
    
    messages = [
        SystemMessage(contennt=system_prompt.strip()),
        HumanMessage(content=question)    
    ]
    return openai_model(messages).content

def get_limited_context(question: str, max_tokens=1500):
    chunks = retrieve_relevant_chunks(question, k=10)
    context = ""
    total_tokens = 0

    for chunk in chunks:
        token_count = len(chunk.split())
        if total_tokens + token_count > max_tokens:
            break
        context += chunk + "\n\n"
        total_tokens += token_count

    return context
