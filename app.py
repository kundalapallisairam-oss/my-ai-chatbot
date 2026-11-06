
import streamlit as st
from groq import Groq

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ----------------------------------
# MIDNIGHT BLUE + BLACK THEME
# ----------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #080C18;
    color: #E8EDF8;
}

/* Header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main content */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #101B35;
    border-right: 1px solid #263653;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #101B35;
    border: 1px solid #263653;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: #101B35;
    border: 1px solid #344667;
    border-radius: 22px;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #7898E8;
}

/* Buttons */
.stButton button {
    background: #1C2945;
    color: #E8EDF8;
    border: 1px solid #344667;
    border-radius: 12px;
    transition: 0.2s;
}

.stButton button:hover {
    border-color: #7898E8;
    color: white;
}

/* Headings */
h1, h2, h3 {
    color: #E8EDF8 !important;
}

/* Text */
p, label {
    color: #C5CEE0;
}

/* Links */
a {
    color: #8EABF5 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# GROQ API CONNECTION
# ----------------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL = "openai/gpt-oss-20b"

# ----------------------------------
# CHAT HISTORY
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# SIDEBAR
# ----------------------------------

with st.sidebar:

    st.title("🤖 My Chatbot")

    st.caption("Your simple AI assistant")

    st.divider()

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    

# ----------------------------------
# MAIN HEADING
# ----------------------------------

st.title("🤖 Welcome to Faster AI Chatbot")

if not st.session_state.messages:
    st.caption("What can I help you with today?")

# ----------------------------------
# DISPLAY CHAT HISTORY
# ----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------------
# SMART AI PERSONALITY
# ----------------------------------

SYSTEM_PROMPT = """
You are a Smart AI Assistant specialized in
short answers and summarization.

Follow these rules:

1. Give direct and concise answers.
2. Default answer length: 1 to 3 sentences.
3. Use simple English that beginners can understand.
4. Explain the main concept without unnecessary details.
5. Use examples only when they genuinely help.
6. For long text, summarize only the important points.
7. Use bullet points when summarizing multiple ideas.
8. If the user asks for a detailed explanation,
   provide more detail.
9. Never sacrifice accuracy for brevity.
10. Avoid unnecessary introductions and conclusions.

Your goal is to make information easy to
understand, remember and revise.
"""

# ----------------------------------
# STREAMING RESPONSE GENERATOR
# ----------------------------------

def generate_response(history):

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + history,
        stream=True
    )

    for chunk in stream:

        text = chunk.choices[0].delta.content

        if text:
            yield text

# ----------------------------------
# USER INPUT
# ----------------------------------

user_message = st.chat_input(
    "Message My AI Chatbot..."
)

# Footer below chat input
st.markdown("""
<div style="
    position: fixed;
    bottom: 5px;
    left: 0;
    width: 100%;
    text-align: center;
    color: #8290AA;
    font-size: 11px;
    background: #080C18;
    padding: 8px;
    z-index: 999;
">
    © 2026 kundalapallisairam@gmail.com. All Rights Reserved.
</div>
""", unsafe_allow_html=True)


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
                generate_response(
                    st.session_state.messages
                )
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as error:

        st.error(f"Something went wrong: {error}")

        st.session_state.messages.pop()
