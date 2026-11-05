
import streamlit as st
from groq import Groq

# Page setup
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #212121;
    color: white;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

[data-testid="stChatMessage"] {
    border: none;
    background: transparent;
    padding: 12px 10px;
}

[data-testid="stChatInput"] {
    border-radius: 24px;
    background-color: #303030;
    border: 1px solid #444;
}

[data-testid="stSidebar"] {
    background-color: #171717;
}

.stButton button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Groq connection
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "openai/gpt-oss-20b"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 My Chatbot")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Powered by Groq AI")

# Main heading
st.title("🤖 My AI Chatbot")

if not st.session_state.messages:
    st.caption("What can I help you with today?")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Streaming generator
def generate_response(history):

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly and helpful AI chatbot. "
                    "Answer naturally and explain things clearly."
                )
            }
        ] + history,
        stream=True
    )

    # Extract only the actual text from each chunk
    for chunk in stream:
        text = chunk.choices[0].delta.content

        if text:
            yield text

# User input
user_message = st.chat_input("Message My AI Chatbot...")

if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        with st.chat_message("assistant"):

            answer = st.write_stream(
                generate_response(st.session_state.messages)
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as error:
        st.error(f"Something went wrong: {error}")

        # Remove failed user message
        st.session_state.messages.pop()
