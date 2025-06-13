import streamlit as st
import sys
import os

# Prevent torch watcher issues in Streamlit Cloud
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch,torch.classes"
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

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
