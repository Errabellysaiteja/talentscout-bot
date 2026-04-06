TalentScout is an intelligent, context-aware conversational agent designed to streamline the initial screening process for tech recruitment. Built with Python and Streamlit, it dynamically gathers essential candidate information through a structured state machine before seamlessly transitioning into an interactive technical assessment powered by Mistral AI. The bot features real-time UI updates, conversation memory, and robust security guardrails to ensure a professional interview environment.

🚀 Installation Instructions
To run this application locally on your machine, follow these steps:

Clone the repository:

Bash```
git clone https://github.com/Errabellysaiteja/talentscout-bot.git
cd talentscout-bot
Set up a virtual environment (Recommended):
```
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install the required dependencies:
```
Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory and add your Mistral API key:
```
Code snippet
MISTRAL_API_KEY=your_api_key_here
Run the application:
```
Bash
streamlit run app.py
```
📖 Usage Guide
Start the Chat: Open the provided local URL (usually http://localhost:8501) or the live Render demo link.

Follow the Prompts: The bot will ask for your details sequentially (Name, Email, Phone, Experience, Role, Location, and Tech Stack).

Live Dashboard: As you answer, watch the left sidebar automatically build your "Candidate Profile," and the top progress bar track your completion status.

Technical Assessment: Once you provide your tech stack, the bot will generate 3-5 tailored interview questions. You can choose to answer them directly in the chat to receive real-time, context-aware feedback.

End Conversation: At any time, type exit, quit, bye, or stop to gracefully terminate the session and submit your profile.

🛠️ Technical Details
Frontend Framework: Streamlit (v1.32+)

Used for rapid UI prototyping, session state management (st.session_state), and rendering dynamic components like progress bars and typing effects.

Backend LLM: Mistral AI (mistral-small-latest) via the official mistralai v2.0+ Python SDK.

Chosen for its exceptional speed, low latency, and strong adherence to complex system prompts.

Architecture Strategy: * Phase 1 (Data Gathering): A hardcoded Python state machine to ensure 100% reliability and zero API latency while collecting the 7 required data points.

Phase 2 (Interviewing): Dynamic API calls to Mistral, passing the entire conversational history to maintain memory and context.

Deployment: Hosted on Render (Cloud PaaS) with Python pinned to 3.11.8 to ensure cross-platform wheel compatibility.

🧠 Prompt Design Strategy
The prompts were engineered to balance strict constraints with natural conversational flow:

Information Gathering: Handled natively via Python logic to prevent the LLM from overwhelming the user by asking 7 questions at once.

Technical Question Generation: The prompt explicitly restricts the LLM to outputting exactly 3 to 5 scenario-based questions that encompass the four required categories (languages, frameworks, databases, tools) without overwhelming the UI.

The "Interviewer" System Guardrail (Security): To prevent prompt injection (e.g., a candidate asking the bot to write code to pass the interview), a strict System Prompt was injected into the context manager. It forces the LLM to maintain its persona, evaluate answers, and explicitly refuse requests to write code or solve problems for the user.

🚧 Challenges & Solutions
Challenge 1: Managing API Latency and UX Freezes

Issue: Waiting for the LLM to generate all technical questions caused the app to freeze, leading to a poor user experience.

Solution: Implemented a custom text generator function (stream_text) paired with Streamlit's st.write_stream() to simulate a live-typing effect, masking the latency and making the bot feel highly responsive.

Challenge 2: Context Loss During Follow-ups

Issue: After asking the technical questions, the LLM forgot what was said if the user tried to answer them.

Solution: Developed ask_llm_with_context(), a function that parses the entire Streamlit chat history (st.session_state.messages) and maps it to Mistral's required dictionary format ({"role": "user/assistant/system", "content": ...}), giving the bot perfect short-term memory for interactive Q&A.

Challenge 3: Cloud Deployment Versioning Errors

Issue: Deploying to Render caused build failures due to Python 3.14 incompatibilities with the orjson wheel, alongside SDK syntax changes in Mistral v2.0.

Solution: Explicitly pinned the Render environment to PYTHON_VERSION 3.11.8 and refactored the codebase to utilize the newest mistralai.client instantiation methods.
