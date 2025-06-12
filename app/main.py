import streamlit as st
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.vectorizer import TextVectorizer
from utils.rag_llm import RAGLLM

# Page config
st.set_page_config(
    page_title="JivaBot - Jiva Infotech Assistant",
    page_icon="🤖",
    layout="wide"
)

# CSS: Fixed-width input bar, clean chat bubbles, mobile-friendly
st.markdown("""
<style>
.chat-box {
    max-height: calc(100vh - 250px);
    overflow-y: auto;
    padding: 1rem;
}

/* User message */
.user-message {
    background: linear-gradient(to right, #1E1E2E, #2D2D44);
    color: white;
    padding: 12px 16px;
    border-radius: 16px 16px 0 16px;
    margin: 10px 0;
    margin-left: auto;
    max-width: 20%;
    text-align: right;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    word-wrap: break-word;
}

/* Bot message */
.bot-message {
    background: linear-gradient(to right, #2C3E50, #4CA1AF);
    color: white;
    padding: 12px 16px;
    border-radius: 16px 16px 16px 0;
    margin: 10px 0;
    margin-right: auto;
    max-width: 50%;
    text-align: left;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    word-wrap: break-word;
}

/* Fixed input bar */
div[data-testid="stForm"] {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem 2rem;
    background-color: #0e1117;
    z-index: 100;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.4);
}

/* Fixed width input */
.stTextInput > div {
    min-width: 800px;
    max-width: 800px;
    margin: 0 auto;
    margin-left: 500px;
}

.stTextInput > div > input {
    font-size: 16px;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #444;
    background-color: #1e1e1e;
    color: white;
}

/* Send button */
.stButton>button {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #444;
    border-radius: 4px;
}

/* Mobile view */
@media screen and (max-width: 768px) {
    .user-message, .bot-message {
        max-width: 80% !important;
        font-size: 14px;
        padding: 10px 12px;
    }

    .chat-box {
        max-height: calc(100vh - 220px);
        padding: 0.75rem;
    }

    div[data-testid="stForm"] {
        padding: 0.75rem 1rem;
    }

    .stTextInput > div {
        min-width: 95% !important;
        margin: 0 auto;
    }

    .stTextInput > div > input {
        font-size: 14px;
        padding: 10px;
    }

    .stButton > button {
        font-size: 14px;
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_chatbot():
    vectorizer = TextVectorizer()
    vector_store = os.path.join("data", "vector_store.pkl")
    index, chunks, dimension = vectorizer.load_vector_store(vector_store)
    api_key_file = os.path.join("secrets", "openrouter_api_key.txt")
    rag_llm = RAGLLM(api_key_file)
    return vectorizer, index, chunks, rag_llm

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_context" not in st.session_state:
        st.session_state.show_context = False
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

def process_query():
    query = st.session_state.user_input
    if query.strip():
        st.session_state.messages.append({"role": "user", "content": query})
        with st.spinner("Thinking..."):
            vectorizer, index, chunks, rag_llm = load_chatbot()
            results = vectorizer.search(query, index, chunks)
            context_chunks = [chunk for chunk, _ in results]
            if st.session_state.show_context:
                with st.expander("Retrieved Context"):
                    for i, (chunk, score) in enumerate(results, 1):
                        st.markdown(f"**Chunk {i}** (relevance: {score:.2f})")
                        st.markdown(chunk)
            response = rag_llm.generate_response(query, context_chunks)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""

def main():
    st.title("🤖 JivaBot")
    st.subheader("Your AI Assistant for Jiva Infotech")

    initialize_session_state()

    with st.sidebar:
        st.markdown("### Settings")
        st.session_state.show_context = st.checkbox(
            "Show retrieved context", value=st.session_state.show_context
        )

    with st.container():
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.text_input(
                "Message", key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        with col2:
            st.form_submit_button("Send", on_click=process_query)

if __name__ == "__main__":
    main()
