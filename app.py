import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage,AIMessage
import uuid

# ==========================================
# Utility Functions
# ==========================================
def generate_thread_id():
    return str(uuid.uuid4())

# ==========================================
# Session Setup
# ==========================================
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()



# ==========================================
# Custom CSS for Classy ChatGPT UI
st.set_page_config(
    page_title="Chemical Expert",
    page_icon="🧪",
    layout="wide",
)

st.markdown("""
<div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
    <h1 style="margin-bottom:0;">🧪 Chemical Expert</h1>
    <p style="color:#b0b0b0; font-size:1rem;">
        AI-powered Chemical Engineering Knowledge Assistant
    </p>
</div>
<hr style="border:0.5px solid #333;">
""", unsafe_allow_html=True)

# ==========================================
st.markdown("""
<style>
/* ---------- Global ---------- */
body {
    background-color: #0f1117;
    color: #e6e6e6;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background-color: #161a22;
    border-right: 1px solid #2a2f3a;
}

/* ---------- Chat Container ---------- */
.chat-container {
    max-width: 900px;
    margin: auto;
    padding: 1.5rem 0;
}

/* ---------- Message Bubbles ---------- */
.user-bubble {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: #fff;
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 4px 16px;
    margin: 0.6rem 0;
    max-width: 75%;
    margin-left: auto;
    font-size: 0.95rem;
}

.assistant-bubble {
    background-color: #1f2937;
    color: #e5e7eb;
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 16px 4px;
    margin: 0.6rem 0;
    max-width: 75%;
    margin-right: auto;
    font-size: 0.95rem;
    border: 1px solid #2a2f3a;
}

/* ---------- Buttons ---------- */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.45rem 1.2rem;
    font-weight: 500;
}
.stButton>button:hover {
    background-color: #1d4ed8;
}

/* ---------- Input ---------- */
textarea, input {
    background-color: #111827 !important;
    color: #e5e7eb !important;
}
</style>
""", unsafe_allow_html=True)






# ==========================================
# Main Chat Section
# ==========================================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state['message_history']:
    if message['role'] == 'user':
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)


    thread_id = st.session_state['thread_id']


    # Generate assistant response
    config = {'configurable': {'thread_id': thread_id}}
    with st.spinner("Thinking..."):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    config=config,
                    stream_mode='messages'

            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content


        ai_message = st.write_stream(ai_only_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
