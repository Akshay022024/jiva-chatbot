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

# CSS: Beautiful chat bubbles and modern UI
st.markdown("""
<style>
/* Main container */
.main .block-container {
    padding-bottom: 120px;
}

/* Chat messages container */
.chat-container {
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 1rem 0;
}

/* User message bubble */
.user-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 25px 25px 8px 25px;
    margin: 10px 0 10px auto;
    max-width: 75%;
    width: fit-content;
    position: relative;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    font-size: 0.95rem;
    line-height: 1.4;
    word-wrap: break-word;
    animation: slideInRight 0.3s ease-out;
}

/* Bot message bubble */
.bot-bubble {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 25px 25px 25px 8px;
    margin: 10px auto 10px 0;
    max-width: 85%;
    width: fit-content;
    position: relative;
    box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
    font-size: 0.95rem;
    line-height: 1.4;
    word-wrap: break-word;
    animation: slideInLeft 0.3s ease-out;
}

/* Animations */
@keyframes slideInRight {
    from { transform: translateX(50px); opacity: 0; scale: 0.8; }
    to { transform: translateX(0); opacity: 1; scale: 1; }
}

@keyframes slideInLeft {
    from { transform: translateX(-50px); opacity: 0; scale: 0.8; }
    to { transform: translateX(0); opacity: 1; scale: 1; }
}

/* Hover effects */
.message-bubble:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
}

/* Input container - fixed at bottom */
.stChatInputContainer, div[data-testid="stChatInputContainer"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border-top: 1px solid #e0e0e0 !important;
    padding: 15px 20px !important;
    z-index: 999 !important;
}

/* Chat input styling */
.stChatInput input {
    border-radius: 25px !important;
    border: 2px solid #667eea !important;
    padding: 12px 20px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.stChatInput input:focus {
    border-color: #f093fb !important;
    box-shadow: 0 0 15px rgba(102, 126, 234, 0.3) !important;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2, #667eea);
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

def main():
    """Main function to run the Streamlit app."""
    st.title("🤖 JivaBot")
    st.subheader("Your AI Assistant for Jiva Infotech")

    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.session_state.show_context = st.checkbox(
            "Show retrieved context",
            value=st.session_state.show_context
        )
        
        st.markdown("---")
        st.markdown("### 🤖 About JivaBot")
        
        st.markdown("""
        **JivaBot** is your intelligent AI assistant designed specifically for Jiva Infotech. 
        
        🎯 **What I can help you with:**
        - Information about Jiva Infotech services
        - Company policies and procedures
        - Technical documentation queries
        - General business inquiries
        
        🧠 **How I work:**
        - I use advanced AI to understand your questions
        - I search through Jiva Infotech's knowledge base
        - I provide accurate, contextual answers
        
        💡 **Tips for better results:**
        - Ask specific questions
        - Use clear, descriptive language
        - Feel free to ask follow-up questions
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        
        st.markdown("""
        ✨ **Smart Context Retrieval**  
        📱 **Mobile-Friendly Design**  
        🎨 **Beautiful Chat Interface**  
        ⚡ **Fast Response Times**  
        🔒 **Secure & Private**
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Chat Statistics")
        message_count = len(st.session_state.messages)
        st.metric("Messages", message_count)
        
        if message_count > 0:
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            st.metric("Questions Asked", user_messages)
            st.metric("Responses Given", bot_messages)

    # Chat container - Display all messages
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 50px 20px; color: #666; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; margin: 20px 0;">
                <h3>👋 Welcome to JivaBot!</h3>
                <p>I'm here to help you with information about Jiva Infotech.</p>
                <p>Ask me anything about our services, policies, or procedures!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display chat messages with proper styling
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                # User message - aligned right with avatar
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 20px 0; align-items: flex-end;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px 22px; border-radius: 25px 25px 8px 25px; max-width: 70%; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); animation: slideInRight 0.4s ease-out; font-size: 0.95rem; line-height: 1.5; word-wrap: break-word; position: relative; margin-right: 10px;">
                        {message["content"]}
                        <div style="position: absolute; bottom: -6px; right: 15px; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-top: 8px solid #764ba2;"></div>
                    </div>
                    <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.8rem; box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);">
                        👤
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Bot message - aligned left with avatar (Professional blue-green theme)
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 20px 0; align-items: flex-end;">
                    <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #4facfe, #00f2fe); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.9rem; box-shadow: 0 3px 10px rgba(79, 172, 254, 0.3); margin-right: 10px;">
                        🤖
                    </div>
                    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 16px 22px; border-radius: 25px 25px 25px 8px; max-width: 75%; box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4); animation: slideInLeft 0.4s ease-out; font-size: 0.95rem; line-height: 1.5; word-wrap: break-word; position: relative;">
                        {message["content"]}
                        <div style="position: absolute; bottom: -6px; left: 15px; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-top: 8px solid #00f2fe;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Chat input - modern Streamlit chat input
    if user_input := st.chat_input("Ask me anything about Jiva Infotech..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        try:
            # Check if this is the first message (excluding welcome)
            user_message_count = len([m for m in st.session_state.messages if m["role"] == "user"])
            is_first_message = user_message_count == 1
            
            if is_first_message:
                # Special loading message for first query
                with st.spinner("🚀 Setting up JivaBot... Loading AI models, processing knowledge base, and preparing everything for you. This may take a moment for the first query. Please be patient! ⏳"):
                    vectorizer, index, chunks, rag_llm = load_chatbot()
                    results = vectorizer.search(user_input, index, chunks)
                    context_chunks = [chunk for chunk, _ in results]
                    
                    if st.session_state.show_context:
                        with st.expander("Retrieved Context"):
                            for i, (chunk, score) in enumerate(results, 1):
                                st.markdown(f"**Chunk {i}** (relevance: {score:.2f})")
                                st.markdown(chunk)
                    
                    response = rag_llm.generate_response(user_input, context_chunks)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                # Regular loading message for subsequent queries
                with st.spinner("💭 Thinking..."):
                    vectorizer, index, chunks, rag_llm = load_chatbot()
                    results = vectorizer.search(user_input, index, chunks)
                    context_chunks = [chunk for chunk, _ in results]
                    
                    if st.session_state.show_context:
                        with st.expander("Retrieved Context"):
                            for i, (chunk, score) in enumerate(results, 1):
                                st.markdown(f"**Chunk {i}** (relevance: {score:.2f})")
                                st.markdown(chunk)
                    
                    response = rag_llm.generate_response(user_input, context_chunks)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
        except Exception as e:
            error_msg = str(e)
            if "payment required" in error_msg.lower() or "402" in error_msg:
                st.error("💳 **Payment Required** - Your OpenRouter API key doesn't have sufficient credits.")
            elif "invalid api key" in error_msg.lower() or "401" in error_msg:
                st.error("🔑 **Invalid API Key** - Please check your OpenRouter API key configuration.")
            elif "rate limit" in error_msg.lower() or "429" in error_msg:
                st.error("⏰ **Rate Limit Exceeded** - Please wait a moment and try again.")
            else:
                st.error(f"🚨 **Error**: {error_msg}")
            
            # Add fallback message
            fallback_response = "I'm sorry, I'm experiencing technical difficulties right now. Please try again later."
            st.session_state.messages.append({"role": "assistant", "content": fallback_response})
        
        # Rerun to update the chat display
        st.rerun()

if __name__ == "__main__":
    main()
