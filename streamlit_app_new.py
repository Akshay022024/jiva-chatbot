import os
import sys
import warnings

# Comprehensive torch watcher prevention
os.environ.update({
    "STREAMLIT_WATCHER_IGNORE_MODULES": "torch,torch.classes,torch.jit,torch.nn,torch.utils",
    "STREAMLIT_SERVER_RUN_ON_SAVE": "false",
    "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
    "STREAMLIT_GLOBAL_DISABLE_WATCHDOG_WARNING": "true",
    "TORCH_DISABLE_WATCHDOG": "1",
    "TORCH_JIT_DISABLE_WATCHDOG": "1",
    "PYTHONUNBUFFERED": "1"
})

# Suppress all warnings
warnings.filterwarnings('ignore')

# Add current directory to path before any other imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import streamlit as st

# Set Streamlit page config first
st.set_page_config(
    page_title="JivaBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from app.main import main
    main()
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please check that all required files are present and dependencies are installed.")
    st.stop()
except Exception as e:
    st.error(f"Application error: {e}")
    st.error("Please check the logs for more details.")
    st.stop()
