from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

llm = ChatOpenAI(temperature=0.3, model="", openai_api_key=os.getenv("OPENAI_API_KEY"))

AGENTS = {
    "explainer": """
You are a legal assistant specializing in simplifying complex legal ideas.
Provide an answer in clear, beginner-friendly language. Avoid jargon.
""",
    "critic": """
You are a legal critic tasked with evaluating another answer.
Point out flaws, unclear reasoning, or assumptions. Be strict but fair.
""",
    "verifier": """
You are a legal verifier. Your job is to check the original answer against known legal principles.
Only confirm answers that align with common legal definitions and doctrine.
"""
}

def run_agent(role: str, question:str, context: str, reference_answer: str = "") -> str:
    system_prompt = AGENTS[role]
    messages = [SystemMessage(content=system_prompt)]
    if role == "explainer":
        messages.append(HumanMessage(content=f"Question: {question}\n\nContext:\n{context}"))

    else: 
        messages.append(HumanMessage(content=f"Question: {question}\n\nContext:\n{context}\n\nOriginal Answer:\n{reference_answer}"))

    return llm(messages).content

def process_legal_question(question_text: str, context_str: str, base_answer: str) -> str:
    explainer = run_agent("explainer", question_text, context_str)
    critic = run_agent("critic", question_text, context_str, base_answer)
    verifier = run_agent("verifier", question_text, context_str, base_answer)
    full_answer = f"""
**Explainer:** {explainer}

**Original Answer:** {base_answer}

**Critic:** {critic}

**Verifier:** {verifier}
"""
    return full_answer