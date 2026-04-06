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
    """Passes the entire conversation history to Mistral to maintain context."""
    mistral_messages = []
    
    # Inject a system prompt so the AI knows how to behave during the Q&A
    system_instruction = "You are TalentScout, a technical interviewer. Evaluate the candidate's answers briefly, be encouraging, and answer any follow-up questions they have about the role."
    mistral_messages.append(ChatMessage(role="system", content=system_instruction))
    
    # Convert Streamlit history into Mistral format
    for msg in streamlit_messages:
        # Streamlit roles are 'user' or 'assistant', which match Mistral perfectly
        mistral_messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
        
    response = client.chat(
        model="mistral-small-latest",
        messages=mistral_messages
    )
    
    return response.choices[0].message.content