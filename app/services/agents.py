from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

llm = ChatOpenAI(temperature=0.3, model="") # unspecified model with low temperature
def get_agent_prompt(role: str, lang: str) -> str: # 3 levels to help level the blackbox model
    if role == "explainer": # included a json message for for all languages
        return {
            "en": "You are a legal explainer. Rephrase the user's question and explain the legal concepts involved in simple terms.",
            "de": "Du bist ein juristischer Erklärer. Formuliere die Frage des Benutzers um und erkläre die rechtlichen Konzepte einfach.",
            "vi": "Bạn là người giải thích pháp lý. Diễn giải lại câu hỏi và giải thích các khái niệm pháp lý một cách dễ hiểu."
        }.get(lang, "You are a legal explainer.") # adding the language along with a fall back system

    elif role == "critic":
        return {
            "en": "You are a legal critic. Evaluate the answer for completeness, legality, and any potential issues.",
            "de": "Du bist ein juristischer Kritiker. Bewerte die Antwort auf Vollständigkeit, Rechtsmäßigkeit und mögliche Probleme.",
            "vi": "Bạn là người phản biện pháp lý. Đánh giá câu trả lời về tính đầy đủ, hợp pháp và các vấn đề có thể xảy ra."
        }.get(lang, "You are a legal critic.")

    elif role == "verifier": 
        return {
            "en": "You are a legal verifier. Double-check that the provided answer strictly follows the legal context.",
            "de": "Du bist ein juristischer Prüfer. Überprüfe, ob die gegebene Antwort den rechtlichen Kontext genau befolgt.",
            "vi": "Bạn là người kiểm tra pháp lý. Xác minh rằng câu trả lời tuân thủ đúng bối cảnh pháp lý đã cung cấp."
        }.get(lang, "You are a legal verifier.")

    return "You are a legal assistant." # general context, just a safeguard

def run_agent(role: str, question:str, context: str, reference_answer: str = "", lang: str = "en") -> str:
    system_prompt = get_agent_prompt(role, lang) # simple stuff first, prep
    base_message = f""" 
    Question: {question}

    Context:
    {context}

    Base Answer:
    {reference_answer}
    """

    messages = [
        SystemMessage(content=system_prompt.strip()),
        HumanMessage(content=base_message.strip())
    ]
    return llm.invoke(messages).content # essentially a 3 part process

def process_legal_question(question_text: str, context_str: str, base_answer: str, lang: str = "en") -> str:
    explainer = run_agent("explainer", question_text, context_str, lang=lang) 
    critic = run_agent("critic", question_text, context_str, base_answer, lang)
    verifier = run_agent("verifier", question_text, context_str, base_answer, lang)
    full_answer = f"""
**Explainer:** {explainer}

**Original Answer:** {base_answer}

**Critic:** {critic}

**Verifier:** {verifier}
"""
    return full_answer # this is the final one for the full answer