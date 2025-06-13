# 🤖 JivaBot – RAG-Based AI Chatbot for Jiva Infotech

JivaBot is a **lightweight but powerful chatbot** that answers user questions based on real content scraped from [jivainfotech.com](https://www.jivainfotech.com/). It uses **web crawling**, **vector search**, and **Mixtral 8x7B via OpenRouter** to provide **highly relevant answers** in real-time with full chat history.

## 🚀 Features

✅ Streamlit UI with chat history  
✅ Web crawling from Jiva Infotech website  
✅ FAISS vector search using embeddings  
✅ RAG (Retrieval-Augmented Generation)  
✅ Mixtral LLM via OpenRouter API (only key needed)  
✅ Fully open-source stack  
✅ Clean, readable codebase  
✅ Optimized for Streamlit Cloud deployment

## 🧱 Project Structure

```
JivaBot/
├── app/
│   └── main.py                 # Streamlit UI with chat interface
├── data/
│   └── website_data.txt        # Crawled raw text from Jiva Infotech
├── utils/
│   ├── web_crawler.py          # Scrapes the website
│   ├── vectorizer.py           # Chunks text & builds embeddings
│   └── rag_llm.py              # RAG logic using Mixtral
├── .streamlit/
│   └── secrets.toml            # API key configuration
├── requirements.txt
├── streamlit_app.py            # Main entry point
└── README.md
```

## 🛠️ Tech Stack

| Component         | Tool / Library                      |
|------------------|-------------------------------------|
| UI               | Streamlit                           |
| Crawling         | requests + BeautifulSoup             |
| Embeddings       | sentence-transformers (`all-MiniLM`)|
| Vector DB        | FAISS                               |
| LLM              | Mixtral 8x7B via OpenRouter          |
| Chat Logic       | Python, Prompt Engineering           |
| Deployment       | Streamlit Cloud                     |

## 🔐 API Key Setup

### For Local Development:
### 🔑 **Get Your API Key:**
1. Create a free account at: [https://openrouter.ai](https://openrouter.ai)  
2. Go to "API Keys" section in your dashboard
3. Create a new API key
4. Copy the API key (starts with `sk-or-`)

### 🏠 **For Local Development:**
Copy the secrets template and add your API key:
```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```
Then edit `.streamlit/secrets.toml`:
```toml
[openrouter]
api_key = "sk-or-xxxxxxxxxxxxxxxxxx"
```

### ☁️ **For Streamlit Cloud Deployment:**
1. Go to your Streamlit Cloud app dashboard
2. Click ⚙️ **Settings**
3. Go to **Secrets** tab
4. Add this configuration:
```toml
[openrouter]
api_key = "sk-or-xxxxxxxxxxxxxxxxxx"
```

## 🧠 How RAG Works

RAG = Retrieval-Augmented Generation

1. Crawl and clean website content
2. Break into small chunks (400 tokens)
3. Embed using Sentence Transformers
4. Store in FAISS (vector search index)

On user query:
1. Embed query
2. Retrieve Top-K similar chunks
3. Build prompt with context
4. Send to Mixtral via OpenRouter
5. Return response to user

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Connect to Streamlit Cloud
3. Add your OpenRouter API key to secrets
4. Deploy!

### Local Development
```bash
git clone https://github.com/Akshay022024/jiva-chatbot.git
cd jiva-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## 💬 Chat Interface

- Message style like WhatsApp
- Scrollable full history
- Answers backed by actual crawled content
- Optional context preview toggle
- Responsive design for mobile and desktop

## 🔒 Notes

- Only queries related to Jiva Infotech will return relevant results
- The vector store is created automatically from the website data
- All dependencies are optimized for cloud deployment
