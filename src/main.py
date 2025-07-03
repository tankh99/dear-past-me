import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set your OpenRouter or DeepSeek API key here or via environment variable
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key")

# Initialize OpenAI client
client = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=OPENAI_API_KEY,
)

def query_llm(prompt: str) -> str:
    # You can change the model to any available on OpenRouter (e.g., deepseek/deepseek-chat)
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # or "deepseek/deepseek-chat", etc.
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

st.title("💬 Custom LLM Chatbot")

# Chat history stored in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def send_message():
    user_input = st.session_state['user_input']
    if user_input:
        response = query_llm(user_input)
        st.session_state['chat_history'].append((user_input, response))
        st.session_state['user_input'] = ""  # This is safe inside the callback

st.text_input("Enter your prompt:", key="user_input")
st.button("Send", on_click=send_message)

st.subheader("Chat History")
for user, bot in st.session_state['chat_history']:
    st.markdown(f"**You:** {user}")
    st.markdown(f"**Bot:** {bot}")
    st.markdown("---")