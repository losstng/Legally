from app.services.llm import ask_legal_question_with_context
from app.services.agents import process_legal_question
from app.utils.language import detect_language

def generate_full_answer(question: str, context: str) -> tuple[str, str, str]: # will get returned in tuple
    lang = detect_language(question) # detect language of the str
    base = ask_legal_question_with_context(question, context, lang) # this is the base answer without going through the 3 critics yet
    full = process_legal_question(question, context, base, lang) #everything has gone through this
    return base, full, lang # tuple