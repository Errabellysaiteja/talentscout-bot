import streamlit as st
import time

from utils import ask_llm, ask_llm_with_context
# Import your actual Mistral logic and prompts!
from utils import ask_llm
from prompts import generate_questions_prompt

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def stream_text(text, delay=0.015):
    """Yields text chunk by chunk to simulate typing."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(delay)

# ==========================================
# 1. INITIALIZE STATE
# ==========================================
st.set_page_config(page_title="TalentScout Assistant", page_icon="🤖")
st.title("🤖 TalentScout Hiring Assistant")

if "step" not in st.session_state:
    st.session_state.step = "name"
    st.session_state.candidate = {}

if "messages" not in st.session_state:
    # We define the message as a variable first to keep the code clean
    greeting_msg = (
        "Hello! 👋 I'm TalentScout, your AI Hiring Assistant. \n\n"
        "**My purpose is to guide you through our initial screening process.** "
        "I will gather some basic details about your background, and then ask a few technical "
        "questions based on your specific tech stack to help our team match you with the best roles.\n\n"
        "Let's get started! What is your full name?"
    )
    
    st.session_state.messages = [
        {"role": "assistant", "content": greeting_msg}
    ]
  

# ==========================================
# 2. RENDER UI ELEMENTS
# ==========================================

# --- SIDEBAR DASHBOARD ---
with st.sidebar:
    st.header("📝 Your Profile")
    if not st.session_state.candidate:
        st.info("Your profile will appear here as we chat.")
    else:
        for key, value in st.session_state.candidate.items():
            clean_key = key.replace("_", " ").title()
            st.write(f"**{clean_key}**: {value}")

# --- PROGRESS BAR ---
flow_stages = ["name", "email", "phone", "experience", "role", "location", "tech", "interview" , "done"]
current_index = flow_stages.index(st.session_state.step)
progress_percentage = current_index / (len(flow_stages) - 1)
st.progress(progress_percentage, text="Screening Progress")

# ==========================================
# 3. RENDER CHAT AND LOGIC
# ==========================================

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    step = st.session_state.step
    response = ""

    if user_input.lower() in ["exit", "quit", "bye", "stop"]:
        response = "Thank you for your time! Our team will contact you soon. You can close this window."
        st.session_state.step = "done"

    elif step == "name":
        st.session_state.candidate["name"] = user_input
        response = f"Nice to meet you, {user_input}! Please enter your email address."
        st.session_state.step = "email"

    elif step == "email":
        st.session_state.candidate["email"] = user_input
        response = "Got it. Please enter your phone number."
        st.session_state.step = "phone"

    elif step == "phone":
        st.session_state.candidate["phone"] = user_input
        response = "How many years of professional experience do you have?"
        st.session_state.step = "experience"

    elif step == "experience":
        st.session_state.candidate["experience"] = user_input
        response = "What is your desired role or position?"
        st.session_state.step = "role"

    elif step == "role":
        st.session_state.candidate["role"] = user_input
        response = "Where are you currently located?"
        st.session_state.step = "location"

    elif step == "location":
        st.session_state.candidate["location"] = user_input
        
        # Explicitly hitting the "Tech Stack Declaration" rubric requirement
        response = (
            "Great! Finally, let's talk about your technical expertise. \n\n"
            "Please specify your **tech stack**, including:\n"
            "- **Programming languages** (e.g., Python, Java)\n"
            "- **Frameworks** (e.g., Django, React)\n"
            "- **Databases** (e.g., PostgreSQL, MongoDB)\n"
            "- **Tools** you are proficient in (e.g., AWS, Docker, Git)"
        )
        st.session_state.step = "tech"

    elif step == "tech":
        st.session_state.candidate["tech_stack"] = user_input
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your tech stack and generating custom questions..."):
                
                # --- ACTUAL MISTRAL AI INTEGRATION ---
                prompt = generate_questions_prompt(user_input)
                
                try:
                    questions = ask_llm(prompt)
                except Exception as e:
                    questions = f"(Error connecting to Mistral AI: {e}. Please check your API key.)"
                # -------------------------------------
                
            response = f"Thanks! Based on your stack, here are a few technical questions:\n\n{questions}\n\n*Type 'exit' to finish.*"
            st.write_stream(stream_text(response))
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.step = "interview"
        st.rerun() 
    elif step == "interview":
        # The user is now answering the questions or asking follow-ups!
        with st.chat_message("assistant"):
            with st.spinner("Evaluating your response..."):
                # We pass the ENTIRE message history to the LLM so it has context
                interview_response = ask_llm_with_context(st.session_state.messages)
                
            st.write_stream(stream_text(interview_response))
            
        st.session_state.messages.append({"role": "assistant", "content": interview_response})
        # We DO NOT change the step here. The user stays in the 'interview' loop 
        # until they type 'exit' (which we already handle at the top of the script!)
        st.rerun()

    elif step == "done":
        response = "Thank you! Your profile has been submitted."

    if step != "tech":
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()