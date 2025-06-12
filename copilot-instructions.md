
---

### ✅ `copilot-instructions.md`

```markdown
# 🧠 Copilot Instructions for JivaBot

---

## 🎯 Objective

Build a chatbot using the following steps:
- Crawl content from [https://www.jivainfotech.com/](https://www.jivainfotech.com/)
- Generate embeddings and save with FAISS
- Accept user queries via Streamlit
- Use RAG to retrieve relevant chunks
- Send full prompt to Mixtral LLM via OpenRouter API
- Display results in a clean chat format with history

---

## 🗂️ Module Responsibilities

### 1. `web_crawler.py`
- Use `requests` + `BeautifulSoup`
- Crawl all links under `https://www.jivainfotech.com/`
- Remove scripts, footers, nav bars
- Save clean text in `data/website_data.txt`

### 2. `vectorizer.py`
- Load raw text  
- Split into chunks (approx. 400 tokens each)  
- Embed using `sentence-transformers/all-MiniLM-L6-v2`  
- Store vectors + texts in FAISS and save as `vector_store.pkl`

### 3. `rag_llm.py`
- Read API key from `secrets/openrouter_api_key.txt`  
- On query:
  - Embed input
  - Retrieve top-K chunks
  - Build a RAG prompt:
    ```
    You are a helpful assistant for Jiva Infotech.
    
    Context:
    {{ chunks }}

    Question:
    {{ user input }}
    ```
  - Send to OpenRouter with Mixtral endpoint
  - Return answer string

### 4. `main.py` (Streamlit App)
- Load vector store on app launch
- Accept input via Streamlit textbox
- Store chat history in `st.session_state`
- Use markdown + styled HTML for bubble chat display
- Handle loading spinner while waiting for Mixtral reply

---

## 🔐 API Endpoint

**POST** `https://openrouter.ai/api/v1/chat/completions`

**Headers:**

Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json

css
Copy
Edit

**Body:**
```json
{
  "model": "mistralai/mixtral-8x7b-instruct",
  "messages": [
    {
      "role": "user",
      "content": "Answer this using context: [ ... ]"
    }
  ]
}
✅ Final Output
Fully working chatbot at localhost:8501

Web content-backed answers

OpenRouter used securely

No vendor lock-in (can swap model easily)

🤖 Additional Tips
Use retry logic in case of API failures

Keep max token limit < 4096

Add context preview (optional toggle in sidebar)