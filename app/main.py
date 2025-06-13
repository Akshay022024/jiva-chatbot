import streamlit as st
import os
import sys
import warnings

# Comprehensive torch watcher prevention - must be set before any imports
os.environ.update({
    "TOKENIZERS_PARALLELISM": "false",
    "STREAMLIT_WATCHER_IGNORE_MODULES": "torch,torch.classes,torch.jit,torch.nn,torch.utils",
    "STREAMLIT_SERVER_RUN_ON_SAVE": "false",
    "TORCH_DISABLE_WATCHDOG": "1",
    "TORCH_JIT_DISABLE_WATCHDOG": "1",
    "PYTHONUNBUFFERED": "1"
})

# Suppress ALL warnings
warnings.filterwarnings("ignore")

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Monkey patch torch to disable watchers if imported
try:
    import torch
    if hasattr(torch, 'jit') and hasattr(torch.jit, '_set_jit_logging'):
        torch.jit._set_jit_logging(False)
except ImportError:
    pass
    os.environ.update({
        "TOKENIZERS_PARALLELISM": "false",
        "STREAMLIT_WATCHER_IGNORE_MODULES": "torch,torch.classes,torch.jit,torch.nn,torch.utils",
        "STREAMLIT_SERVER_RUN_ON_SAVE": "false",
        "TORCH_DISABLE_WATCHDOG": "1",
        "TORCH_JIT_DISABLE_WATCHDOG": "1",
        "PYTHONUNBUFFERED": "1"
    })
    import warnings
    warnings.filterwarnings("ignore")

# Import utilities with error handling
try:
    from utils.vectorizer import TextVectorizer
    from utils.rag_llm import RAGLLM
except ImportError as e:
    st.error(f"Failed to import required modules: {e}")
    st.error("Please ensure all dependencies are installed correctly.")
    st.stop()

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

@st.cache_resource(show_spinner=False)
def load_chatbot():
    """Load the chatbot components with caching."""
    try:
        # Initialize vectorizer with error handling
        with st.spinner("Loading AI models..."):
            vectorizer = TextVectorizer()
        
        # Check if we have the website data
        website_data_path = os.path.join("data", "website_data.txt")
        if not os.path.exists(website_data_path):
            st.error("Error: website_data.txt not found in data directory!")
            st.stop()
            
        # Read the website data
        with open(website_data_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        # Create chunks and embeddings with progress indicator
        with st.spinner("Processing content..."):
            chunks = vectorizer.get_text_chunks(text)
            index, embeddings = vectorizer.create_vector_store(chunks)
        
        # Get API key from Streamlit secrets
        try:
            api_key = st.secrets["openrouter"]["api_key"]
            if not api_key or api_key.strip() == "":
                raise KeyError("API key is empty")
        except KeyError:
            st.error("🔑 **API Key Not Found!**")
            st.error("Please configure your OpenRouter API key in Streamlit Cloud secrets:")
            st.code("""
            [openrouter]
            api_key = "your_actual_api_key_here"
            """)
            st.info("📋 **How to add secrets in Streamlit Cloud:**\n"
                   "1. Go to your app dashboard\n"
                   "2. Click ⚙️ Settings\n"
                   "3. Go to Secrets tab\n"
                   "4. Add the above configuration")
            st.stop()
        
        rag_llm = RAGLLM(api_key)
        
        return vectorizer, index, chunks, rag_llm
        
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        st.stop()

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_context" not in st.session_state:
        st.session_state.show_context = False
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

def process_query():
    """Process the user's query and generate a response."""
    query = st.session_state.user_input
    if query.strip():
        st.session_state.messages.append({"role": "user", "content": query})
        try:
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
        except Exception as e:
            error_msg = str(e)
            if "payment required" in error_msg.lower() or "402" in error_msg:
                st.error("💳 **Payment Required**")
                st.error("Your OpenRouter API key doesn't have sufficient credits.")
                st.info("**To fix this:**\n"
                       "1. Go to [OpenRouter.ai](https://openrouter.ai)\n"
                       "2. Sign in to your account\n"
                       "3. Add credits to your account\n"
                       "4. Or get a new API key with credits")
            elif "invalid api key" in error_msg.lower() or "401" in error_msg:
                st.error("🔑 **Invalid API Key**")
                st.error("Your OpenRouter API key is invalid or expired.")
                st.info("**To fix this:**\n"
                       "1. Get a valid API key from [OpenRouter.ai](https://openrouter.ai)\n"
                       "2. Update your Streamlit secrets with the new key")
            elif "rate limit" in error_msg.lower() or "429" in error_msg:
                st.error("⏰ **Rate Limit Exceeded**")
                st.error("Too many requests. Please wait a moment and try again.")
            else:
                st.error(f"🚨 **Error**: {error_msg}")
                st.info("If this persists, please check your API configuration or try again later.")
            
            # Add a fallback message
            fallback_response = "I'm sorry, I'm experiencing technical difficulties right now. Please try again later or contact support if the issue persists."
            st.session_state.messages.append({"role": "assistant", "content": fallback_response})
            
        st.session_state.user_input = ""

def main():
    """Main function to run the Streamlit app."""
    st.title("🤖 JivaBot")
    st.subheader("Your AI Assistant for Jiva Infotech")

    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### Settings")
        st.session_state.show_context = st.checkbox(
            "Show retrieved context",
            value=st.session_state.show_context
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Configuration Help")
        
        with st.expander("🔑 API Key Setup"):
            st.markdown("""
            **If you're getting payment/API errors:**
            
            1. **Get OpenRouter API Key:**
               - Visit [OpenRouter.ai](https://openrouter.ai)
               - Sign up/Login to your account
               - Generate an API key
               - Add credits to your account
            
            2. **Add to Streamlit Secrets:**
               - Go to your app dashboard
               - Click ⚙️ Settings → Secrets
               - Add this configuration:
               ```
               [openrouter]
               api_key = "your_actual_key_here"
               ```
            
            3. **Restart your app** after adding secrets
            """)
            
        with st.expander("🚨 Troubleshooting"):
            st.markdown("""
            **Common Issues:**
            
            - **402 Payment Required**: Add credits to OpenRouter
            - **401 Unauthorized**: Check API key is correct
            - **429 Rate Limited**: Wait and try again
            - **Timeout**: Check internet connection
            
            **Need Help?**
            Contact the development team if issues persist.
            """)

    # Chat container
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>',
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>',
                           unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input form
    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([6,1])
        with col1:
            st.text_input(
                "Message",
                key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        with col2:
            submit_button = st.form_submit_button("Send", on_click=process_query)

if __name__ == "__main__":
    main()
