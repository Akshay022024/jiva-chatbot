# Streamlit Cloud Deployment Guide

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
1. GitHub repository (already set up)
2. OpenRouter API key from [openrouter.ai](https://openrouter.ai)

### Steps to Deploy

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository: `Akshay022024/jiva-chatbot`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Configure Secrets**
   - In the app settings, go to "Secrets"
   - Add the following:
   ```toml
   [openrouter]
   api_key = "your-openrouter-api-key-here"
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait for the app to build and start

### Troubleshooting

- **Import Errors**: All dependencies are now fixed with compatible versions
- **NumPy Issues**: Fixed with numpy<2.0.0 constraint
- **API Key Issues**: Now uses Streamlit secrets properly
- **Torch Dependencies**: Removed to reduce deployment size

### App Features
- ✅ Real-time chat interface
- ✅ RAG-based responses using Jiva Infotech content
- ✅ Context preview toggle
- ✅ Mobile-responsive design
- ✅ Optimized for cloud deployment

The app should now deploy successfully on Streamlit Cloud!
