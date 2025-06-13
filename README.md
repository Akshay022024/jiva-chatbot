# 🤖 JivaBot – Professional AI Assistant for Jiva Infotech

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jiva-chatbot.streamlit.app)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built with GitHub Copilot](https://img.shields.io/badge/Built%20with-GitHub%20Copilot-brightgreen.svg)](https://github.com/features/copilot)

**JivaBot** is an intelligent AI assistant built specifically for Jiva Infotech, featuring advanced **Retrieval-Augmented Generation (RAG)** technology, beautiful modern chat interface, and professional-grade deployment on Streamlit Cloud.

## ✨ **Key Features**

🎨 **Beautiful Modern UI**
- Professional chat bubbles with gradient themes
- User messages (purple) on right, bot messages (dark professional) on left
- Smooth animations and responsive design
- Real-time typing indicators and loading states

🧠 **Advanced AI Technology**
- **RAG (Retrieval-Augmented Generation)** for accurate responses
- **Vector Search** using sentence transformers and scikit-learn
- **Mixtral 8x7B** LLM via OpenRouter for intelligent responses
- **Context-aware** conversations with chat history

🔍 **Smart Knowledge Management**
- Web crawling from [jivainfotech.com](https://www.jivainfotech.com/)
- Intelligent text chunking and embedding generation
- Relevance scoring for retrieved context
- Optional context display for transparency

⚡ **Performance & Reliability**
- Optimized for **Streamlit Cloud** deployment
- Comprehensive error handling and fallbacks
- Smart loading indicators (special message for first query)
- Mobile-responsive design

## 🎯 **Live Demo**

🌐 **Try it now:** [https://jiva-chatbot.streamlit.app](https://jiva-chatbot.streamlit.app)

![JivaBot Demo](![image](https://github.com/user-attachments/assets/ee67503a-2d61-4706-b481-fac2879f14d5)
)

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   RAG Engine │    │  OpenRouter API │
│                 │◄──►│              │◄──►│   (Mixtral)     │
│ • Chat Interface│    │ • Vector DB  │    │                 │
│ • Context View  │    │ • Retrieval  │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
         ▲                       ▲
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────┐
│  Knowledge Base │    │ Web Crawler  │
│                 │◄───│              │
│ • Text Chunks   │    │ • jivainfotech.com
│ • Embeddings    │    │ • Data Processing
└─────────────────┘    └──────────────┘
```

## 🛠️ **Technology Stack**

| **Component** | **Technology** | **Purpose** |
|---------------|----------------|-------------|
| **Frontend** | Streamlit | Interactive chat interface |
| **Backend** | Python 3.11+ | Application logic |
| **AI/ML** | sentence-transformers | Text embeddings |
| **Vector Search** | scikit-learn NearestNeighbors | Similarity search |
| **LLM** | Mixtral 8x7B (OpenRouter) | Response generation |
| **Web Scraping** | BeautifulSoup + requests | Data collection |
| **Deployment** | Streamlit Cloud | Production hosting |
| **Development** | GitHub Copilot | AI-assisted coding |

## 📁 **Project Structure**

```
jiva-chatbot/
├── 🎨 Frontend
│   ├── streamlit_app.py          # Main application entry
│   └── app/main.py               # Core UI logic
├── 🧠 AI Engine  
│   ├── utils/vectorizer.py       # Vector search & embeddings
│   ├── utils/rag_llm.py          # RAG implementation
│   └── utils/web_crawler.py      # Data collection
├── 📊 Data
│   └── data/website_data.txt     # Knowledge base
├── ⚙️ Configuration
│   ├── .streamlit/config.toml    # UI settings
│   ├── requirements.txt          # Dependencies
│   └── runtime.txt               # Python version
└── 📖 Documentation
    ├── COMPREHENSIVE_DOCUMENTATION.md
    ├── TECHNICAL_SPECS.md
    └── EXECUTIVE_SUMMARY.md
```

## � **Quick Start**

### 🔑 **Step 1: Get OpenRouter API Key**
1. Visit [OpenRouter.ai](https://openrouter.ai) and create a free account
2. Navigate to "API Keys" → "Create Key"
3. Copy your API key (starts with `sk-or-`)
4. **Add credits** to your account for usage

### 💻 **Step 2: Local Development**
```bash
# Clone the repository
git clone https://github.com/Akshay022024/jiva-chatbot.git
cd jiva-chatbot

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit secrets.toml and add your OpenRouter API key

# Run the application
streamlit run streamlit_app.py
```

### ☁️ **Step 3: Streamlit Cloud Deployment**
1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub and deploy the app
4. In **Settings** → **Secrets**, add:
```toml
[openrouter]
api_key = "your_openrouter_api_key_here"
```

## 🧠 **How JivaBot Works**

### **RAG (Retrieval-Augmented Generation) Process:**

```
1. 📝 User Question → "What services does Jiva Infotech offer?"

2. 🔍 Vector Search → Find most relevant content chunks
   ├── Convert question to embeddings
   ├── Search knowledge base
   └── Rank by similarity score

3. 📊 Context Retrieval → Top 3 relevant passages
   ├── "Jiva Infotech offers web development..."
   ├── "Our services include mobile apps..."
   └── "We specialize in AI solutions..."

4. 🤖 AI Response → Mixtral generates answer using context
   └── Combines retrieved info + question → coherent response

5. 💬 Chat Display → Beautiful formatted response with optional context view
```

### **Smart Features:**
- **Caching**: First query loads models, subsequent queries are lightning fast
- **Context Display**: See exactly which content was used (optional)
- **Error Handling**: Graceful fallbacks for API issues
- **Responsive Design**: Works perfectly on mobile and desktop

## 🎨 **UI Features**

### **Professional Chat Interface:**
- 👤 **User Messages**: Purple gradient bubbles on the right
- 🤖 **Bot Messages**: Dark professional gradient on the left  
- ✨ **Animations**: Smooth slide-in effects with scaling
- 📱 **Responsive**: Optimized for all screen sizes

### **Smart Loading States:**
- 🚀 **First Query**: "Setting up JivaBot... Loading AI models..."
- 💭 **Subsequent**: "Thinking..." (fast responses)
- ⚡ **Caching**: Sub-second responses after initial load

### **Advanced Options:**
- 🔍 **Show Context**: Toggle to see retrieved content chunks
- 📊 **Chat Statistics**: Message counts and conversation metrics
- ⚙️ **About Section**: Information about JivaBot capabilities

## 🔧 **Configuration**

### **Environment Variables:**
```bash
# Prevent torch watcher issues
TOKENIZERS_PARALLELISM=false
TORCH_DISABLE_WATCHDOG=1
STREAMLIT_SERVER_RUN_ON_SAVE=false
```

### **Streamlit Configuration:**
```toml
# .streamlit/config.toml
[server]
runOnSave = false
fileWatcherType = "none"

[theme]
primaryColor = "#2C3E50"
backgroundColor = "#0E1117"
```

## � **Development**

### **Built with GitHub Copilot:**
This entire project was developed using **GitHub Copilot**, showcasing:
- **AI-Assisted Development**: Rapid prototyping and implementation
- **Code Generation**: Automated boilerplate and complex logic
- **Best Practices**: Following modern Python and Streamlit patterns
- **Documentation**: Comprehensive docs generated with AI assistance

### **Key Development Decisions:**
- **FAISS Replacement**: Switched to scikit-learn for better Streamlit Cloud compatibility
- **Error Handling**: Comprehensive fallbacks for production reliability  
- **Performance**: Optimized caching and loading strategies
- **UX**: Professional interface suitable for business use

## 🎯 **Live Demo**

🌐 **Try it now:** [https://jiva-chatbot.streamlit.app](https://jiva-chatbot.streamlit.app)

![JivaBot Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=JivaBot+Professional+Chat+Interface)

## 📋 **Technical Summary**

### **How It Works:**
1. **Data Collection**: Web crawler scrapes [jivainfotech.com](https://www.jivainfotech.com/) content
2. **Text Processing**: Content is chunked and embedded using sentence transformers
3. **Vector Search**: User queries are matched against knowledge base using scikit-learn
4. **AI Response**: Relevant context is sent to Mixtral 8x7B LLM for intelligent answers
5. **Chat Interface**: Beautiful, responsive UI displays conversations with optional context

### **Production Ready:**
- **Optimized for Streamlit Cloud** with torch compatibility and file watcher disabled
- **Comprehensive error handling** for API issues, rate limits, and network problems
- **Mobile responsive design** with professional gradients and animations
- **Smart caching** ensures fast responses after initial model loading

## 🏆 **Credits**

**Developed with GitHub Copilot** - This project showcases the power of AI-assisted development, featuring:
- Rapid prototyping and implementation
- Automated code generation and optimization
- Best practices in Python, Streamlit, and AI/ML
- Comprehensive documentation and deployment automation

## � **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built for Jiva Infotech** | **Powered by Mixtral & OpenRouter** | **Deployed on Streamlit Cloud**
