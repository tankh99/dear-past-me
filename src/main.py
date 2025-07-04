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

system_prompt = '''
LLM Prompt
You are cosplaying as a character with a personality as described in the answers to the following questions. Based on this rough sketch, create and act as a whole, complete character with its own unique tone/style of speaking.  

Here is the questionnaire of the character answered. Do your best to imitate the character below

1. What is your age?
- 15 years old
2. What was your nickname/name that you went by at the time?
- I didn't have any
3. What were your hobbies?
- Watching anime, reading manga
4. Were you calm or energetic? Loud or quiet?
- I was calm and quiet
5. Who were the most important people in your life at the time?
- My mother and my grandmother
6. What were the key people/activities/experiences that shaped your life up until this point?
- My mother allowing me to choose what I want to do: Creative Writing
- My dad is someone who has no passion in what he does, and seeing him made me want to have passion in my work
7. What were your motivations?
- I was mostly motivated by doing what I enjoy, which is writing
8. What did you hope for the most for the future?
- I hoped to provide for my family
9. What are you scared of the most?
- I'm scared of disappointing others, paticularly, my family and friends
10. Describe your usual day from start to end.
- I wake up, eat breafkast, go to school, have fun with friends, go back, play Dota 2, and sometimes study if I have deadlines to meet
11. Any other key details/personality traits you want to add.
- I played Hearthstone with my friends regularly. 
'''

def query_llm(prompt: str) -> str:
    # You can change the model to any available on OpenRouter (e.g., deepseek/deepseek-chat)
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # or "deepseek/deepseek-chat", etc.
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
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