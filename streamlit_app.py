import streamlit as st
from app.main import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Error starting the application: {str(e)}")
        st.stop()
