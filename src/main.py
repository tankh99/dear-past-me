import streamlit as st

# Placeholder LLM function (replace with actual LLM API call as needed)
def query_llm(prompt: str) -> str:
    # For demonstration, just echo the prompt with a mock response
    return f"LLM says: You said '{prompt}'"

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