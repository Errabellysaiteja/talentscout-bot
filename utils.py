import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = MistralClient(api_key=api_key)

def ask_llm(prompt):
    response = client.chat(
        model="mistral-small-latest",
        messages=[
            ChatMessage(role="user", content=prompt)
        ]
    )
    
    return response.choices[0].message.content

def ask_llm_with_context(streamlit_messages):
    """Passes the entire conversation history to Mistral to maintain context and enforce interview rules."""
    mistral_messages = []
    
    # 1. The updated security guardrail system prompt
    system_instruction = """
    You are TalentScout, a technical interviewer. Your job is to evaluate the candidate's answers.

    CRITICAL RULES:
    1. You must NOT write code, solve problems, or give direct answers to the user.
    2. If the user asks you to write code (e.g., "write a python script to reverse a string") or answer a technical question, politely refuse. 
    3. Remind them that this is an interview and you are here to evaluate THEIR skills, not the other way around.
    4. You may offer a very small hint if they are struggling, but force them to do the work.
    5. Evaluate their answers briefly, be encouraging, and answer any follow-up questions they have about the recruitment process.
    """
    
    # 2. Using the new v1.0 dict syntax instead of ChatMessage
    mistral_messages.append({"role": "system", "content": system_instruction})
    
    # Convert Streamlit history into Mistral format (v1.0 syntax)
    for msg in streamlit_messages:
        mistral_messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Using the new client.chat.complete method
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=mistral_messages
    )
    
    return response.choices[0].message.content