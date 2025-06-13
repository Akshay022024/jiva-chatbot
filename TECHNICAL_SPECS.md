# 🔧 JivaBot Technical Specifications
## Detailed Technical Documentation for Development Teams

---

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    JivaBot Technical Stack                      │
├─────────────────────────────────────────────────────────────────┤
│  Presentation Layer                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Streamlit UI    │  │ Chat Interface  │  │ Admin Panel     │ │
│  │ Components      │  │ WebSocket Comm  │  │ Configuration   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Session Manager │  │ Query Processor │  │ Response Engine │ │
│  │ State Handling  │  │ Intent Analysis │  │ Context Builder │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  AI/ML Processing Layer                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Vector Search   │  │ LLM Integration │  │ RAG Pipeline    │ │
│  │ Embedding Gen   │  │ Response Gen    │  │ Context Merge   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Data Access Layer                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Knowledge Base  │  │ Vector Store    │  │ Cache Layer     │ │
│  │ File System     │  │ In-Memory Index │  │ Session Data    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

### Directory Layout
```
jiva-chatbot/
├── 📁 app/                          # Core application modules
│   ├── 🐍 main.py                   # Primary application controller
│   └── 🐍 main_backup.py            # Version backup
├── 📁 utils/                        # Utility modules
│   ├── 🐍 rag_llm.py               # LLM integration & response generation
│   ├── 🐍 vectorizer.py            # Vector search and embeddings
│   ├── 🐍 vectorizer_old.py        # Legacy implementation
│   └── 🐍 torch_utils.py           # PyTorch optimization utilities
├── 📁 data/                         # Knowledge base
│   └── 📄 website_data.txt          # Company information corpus
├── 📁 .streamlit/                   # Streamlit configuration
│   ├── ⚙️ config.toml              # Application settings
│   └── 🔒 secrets.toml.template    # Security configuration template
├── 🐍 streamlit_app.py             # Application entry point
├── 📋 requirements.txt              # Python dependencies
├── 📚 README.md                     # Project documentation
├── 📊 COMPREHENSIVE_DOCUMENTATION.md # Complete technical docs
├── 📈 EXECUTIVE_SUMMARY.md          # Business overview
└── 🔧 TECHNICAL_SPECS.md           # This document
```

---

## 🧩 Component Specifications

### 1. Application Controller (`app/main.py`)

#### **Core Functions**
```python
def main() -> None:
    """Primary application entry point with UI rendering"""
    
def load_chatbot() -> Tuple[TextVectorizer, Any, List[str], RAGLLM]:
    """Cached chatbot component initialization"""
    
def initialize_session_state() -> None:
    """Streamlit session state management"""
```

#### **Key Features**
- **Session Management**: Stateful conversation handling
- **UI Rendering**: Professional chat interface with animations
- **Error Handling**: Comprehensive exception management
- **Performance Optimization**: Cached model loading

#### **Technical Details**
```python
# Caching strategy for performance
@st.cache_resource(show_spinner=False)
def load_chatbot():
    # Heavy operations cached across sessions
    vectorizer = TextVectorizer()
    # ... component initialization
    return vectorizer, index, chunks, rag_llm

# Smart loading indicators
def handle_user_query(user_input: str, is_first_message: bool):
    if is_first_message:
        # Detailed setup explanation for first query
        spinner_text = "🚀 Setting up JivaBot... Loading AI models..."
    else:
        # Quick indicator for subsequent queries
        spinner_text = "💭 Thinking..."
```

### 2. RAG LLM Engine (`utils/rag_llm.py`)

#### **Class Structure**
```python
class RAGLLM:
    def __init__(self, api_key: str):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = api_key
    
    def build_prompt(self, query: str, context_chunks: List[str]) -> List[Dict]:
        """Construct RAG-optimized prompts"""
    
    @retry_with_backoff(retries=3, backoff_in_seconds=1)
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """API interaction with retry logic"""
    
    def generate_response(self, query: str, context_chunks: List[str]) -> str:
        """Main response generation pipeline"""
```

#### **Error Handling Matrix**
```python
# Comprehensive API error management
ERROR_HANDLERS = {
    402: "💳 Payment Required - API credits insufficient",
    401: "🔑 Invalid API Key - Check configuration", 
    429: "⏰ Rate Limited - Please wait",
    500: "🔧 Server Error - Try again later",
    "timeout": "⏱️ Request Timeout - Connection issue",
    "connection": "🌐 Connection Error - Network problem"
}
```

### 3. Vector Search Engine (`utils/vectorizer.py`)

#### **Core Implementation**
```python
class TextVectorizer:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = 400  # Optimal chunk size for context
    
    def get_text_chunks(self, text: str) -> List[str]:
        """Intelligent text segmentation"""
    
    def create_vector_store(self, chunks: List[str]) -> Tuple[NearestNeighbors, np.ndarray]:
        """Vector index creation with embeddings"""
    
    def search(self, query: str, index: NearestNeighbors, chunks: List[str]) -> List[Tuple[str, float]]:
        """Semantic similarity search"""
```

#### **Optimization Features**
```python
# Performance optimizations
TORCH_ENV_VARS = {
    "TOKENIZERS_PARALLELISM": "false",      # Prevent threading issues
    "TORCH_DISABLE_WATCHDOG": "1",          # Disable file watching
    "TORCH_JIT_DISABLE_WATCHDOG": "1"       # Disable JIT watching
}

# Embedding model configuration
MODEL_CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "dimensions": 384,                        # Vector dimensions
    "max_length": 512,                       # Token limit
    "normalize": True                        # L2 normalization
}
```

---

## 🎨 Frontend Specifications

### User Interface Components

#### **Chat Bubble System**
```css
/* User message styling */
.user-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 25px 25px 8px 25px;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    animation: slideInRight 0.4s ease-out;
}

/* Bot response styling */
.bot-bubble {
    background: linear-gradient(135deg, #2c3e50 0%, #4a6741 100%);
    border-radius: 25px 25px 25px 8px;
    box-shadow: 0 6px 20px rgba(44, 62, 80, 0.4);
    animation: slideInLeft 0.4s ease-out;
}
```

#### **Animation System**
```css
/* Smooth entry animations */
@keyframes slideInRight {
    from { transform: translateX(50px); opacity: 0; scale: 0.8; }
    to { transform: translateX(0); opacity: 1; scale: 1; }
}

@keyframes slideInLeft {
    from { transform: translateX(-50px); opacity: 0; scale: 0.8; }
    to { transform: translateX(0); opacity: 1; scale: 1; }
}
```

#### **Responsive Design**
```css
/* Mobile optimization */
@media (max-width: 768px) {
    .user-bubble, .bot-bubble {
        max-width: 85% !important;
        font-size: 0.9rem !important;
        padding: 12px 16px !important;
    }
}
```

### State Management

#### **Session Variables**
```python
# Streamlit session state schema
SESSION_STATE = {
    "messages": List[Dict[str, str]],        # Chat history
    "show_context": bool,                    # Context display toggle
    "user_input": str,                       # Current input
    "chatbot_loaded": bool,                  # Initialization flag
    "error_count": int,                      # Error tracking
    "last_query_time": datetime             # Performance monitoring
}
```

---

## 🔧 API Specifications

### OpenRouter Integration

#### **Request Format**
```python
# API request structure
REQUEST_SCHEMA = {
    "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [
        {
            "role": "system",
            "content": "Professional Jiva Infotech assistant prompt"
        },
        {
            "role": "user", 
            "content": "Context: {context}\n\nQuestion: {query}"
        }
    ],
    "max_tokens": 1000,
    "temperature": 0.7,
    "top_p": 0.9
}
```

#### **Response Handling**
```python
# Response processing pipeline
def process_api_response(response: requests.Response) -> str:
    # Status code validation
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        raise APIError(f"Status: {response.status_code}")
```

### Rate Limiting & Retry Logic

#### **Backoff Strategy**
```python
@retry_with_backoff(retries=3, backoff_in_seconds=1)
def api_call_with_retry():
    """Exponential backoff: 1s, 2s, 4s intervals"""
    # Automatic retry with increasing delays
    # Maximum 3 attempts before failure
```

---

## 📊 Performance Specifications

### Benchmarks & Metrics

#### **Response Time Targets**
```python
PERFORMANCE_TARGETS = {
    "first_query_setup": "< 12 seconds",     # Model loading + first inference
    "subsequent_queries": "< 4 seconds",     # Cached model inference
    "ui_responsiveness": "< 100ms",          # Interface updates
    "vector_search": "< 500ms",              # Similarity computation
    "api_response": "< 3 seconds"            # LLM generation
}
```

#### **Resource Requirements**
```python
SYSTEM_REQUIREMENTS = {
    "memory": {
        "base_app": "~100MB",
        "with_models": "~500MB",
        "peak_usage": "~750MB"
    },
    "cpu": {
        "idle": "< 5%",
        "inference": "30-60%",
        "startup": "80-100%"
    },
    "storage": {
        "application": "~50MB",
        "models": "~400MB",
        "cache": "~100MB"
    }
}
```

### Optimization Strategies

#### **Caching Implementation**
```python
# Multi-level caching strategy
@st.cache_resource(show_spinner=False)
def load_models():
    """Cache heavy model loading operations"""

@st.cache_data(ttl=3600)  # 1 hour TTL
def cache_embeddings(text_chunks: List[str]):
    """Cache embedding computations"""

@lru_cache(maxsize=1000)
def cache_search_results(query: str):
    """LRU cache for frequent queries"""
```

---

## 🔒 Security Specifications

### API Security

#### **Secret Management**
```toml
# Streamlit Cloud secrets configuration
[openrouter]
api_key = "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

[security]
enable_cors = false
disable_file_watcher = true
rate_limit_enabled = true
```

#### **Environment Hardening**
```python
# Security environment variables
SECURITY_CONFIG = {
    "STREAMLIT_SERVER_ENABLE_CORS": "false",
    "STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION": "true",
    "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
    "PYTHONUNBUFFERED": "1"
}
```

### Data Protection

#### **Privacy Implementation**
```python
class DataProtection:
    """Privacy-first data handling"""
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Remove sensitive information from queries"""
        
    @staticmethod 
    def secure_logging(message: str) -> None:
        """Log without exposing sensitive data"""
        
    @staticmethod
    def session_cleanup() -> None:
        """Clear sensitive data on session end"""
```

---

## 🚀 Deployment Specifications

### Streamlit Cloud Configuration

#### **App Configuration (`config.toml`)**
```toml
[server]
runOnSave = false
fileWatcherType = "none"
enableCORS = false
maxUploadSize = 200

[theme]
primaryColor = "#667eea"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1E1E1E"
textColor = "#FFFFFF"

[browser]
gatherUsageStats = false

[runner]
magicEnabled = false
```

#### **Dependencies (`requirements.txt`)**
```txt
# Production-optimized dependencies
streamlit>=1.24.0
sentence-transformers>=2.7.0
torch>=2.5.0                    # Python 3.13 compatible
requests>=2.32.0
beautifulsoup4>=4.12.0
numpy<2.0.0                     # Version constraint for compatibility
scikit-learn>=1.3.0
```

### Environment Setup

#### **Development Environment**
```bash
# Local development setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Environment variables
export OPENROUTER_API_KEY="your-api-key"
export STREAMLIT_SERVER_RUN_ON_SAVE=false

# Run application
streamlit run streamlit_app.py
```

#### **Production Deployment**
```yaml
# GitHub Actions workflow (if needed)
name: Deploy to Streamlit Cloud
on:
  push:
    branches: [main]
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit Cloud
        # Automatic deployment via GitHub integration
```

---

## 🔧 Maintenance & Monitoring

### Health Checks

#### **System Monitoring**
```python
def health_check() -> Dict[str, str]:
    """Application health status"""
    return {
        "status": "healthy",
        "model_loaded": str(model_cache_status()),
        "api_connection": str(test_api_connection()),
        "memory_usage": f"{get_memory_usage()}MB",
        "uptime": str(get_uptime())
    }
```

#### **Error Tracking**
```python
class ErrorTracker:
    """Comprehensive error monitoring"""
    
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.error_timestamps = []
    
    def log_error(self, error_type: str, details: str):
        """Track and categorize errors"""
        
    def get_error_summary(self) -> Dict:
        """Generate error analytics"""
```

### Performance Monitoring

#### **Metrics Collection**
```python
METRICS = {
    "query_count": Counter(),
    "response_times": [],
    "error_rates": defaultdict(int),
    "user_satisfaction": [],
    "cache_hit_rates": {}
}
```

---

## 🔄 Update & Maintenance Procedures

### Code Updates

#### **Version Control Workflow**
```bash
# Development workflow
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "feat: description"
git push origin feature/new-feature
# Create pull request
# After review and merge to main, auto-deploy triggers
```

#### **Dependency Updates**
```bash
# Regular dependency maintenance
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
# Test thoroughly before deployment
```

### Data Updates

#### **Knowledge Base Refresh**
```python
def update_knowledge_base(new_content: str) -> None:
    """Update company information corpus"""
    # 1. Backup current data
    # 2. Validate new content
    # 3. Regenerate embeddings
    # 4. Update vector index
    # 5. Test retrieval quality
```

---

## 📋 Testing Specifications

### Unit Testing

#### **Test Coverage Areas**
```python
# Core functionality tests
def test_vectorizer_search():
    """Test semantic search accuracy"""
    
def test_rag_response_generation():
    """Test response quality and relevance"""
    
def test_error_handling():
    """Test graceful error management"""
    
def test_ui_components():
    """Test interface responsiveness"""
```

### Integration Testing

#### **End-to-End Scenarios**
```python
TEST_SCENARIOS = [
    {
        "name": "Happy path query",
        "input": "What services does Jiva Infotech offer?",
        "expected": "Professional response with relevant context"
    },
    {
        "name": "API failure handling", 
        "input": "Test query with API unavailable",
        "expected": "Graceful fallback response"
    }
]
```

---

## 🎯 Quality Assurance

### Code Quality Standards

#### **GitHub Copilot Integration Points**
```python
# Areas where Copilot provided significant value:
COPILOT_CONTRIBUTIONS = {
    "code_generation": "60% of total codebase",
    "error_handling": "Comprehensive exception patterns",
    "ui_styling": "Advanced CSS animations and responsive design",
    "api_integration": "Robust retry logic and error management",
    "documentation": "Detailed docstrings and comments",
    "optimization": "Performance tuning suggestions"
}
```

#### **Best Practices Implemented**
- **Clean Code**: Readable, maintainable structure
- **Error Handling**: Comprehensive exception management  
- **Security**: Best practices for API and data handling
- **Performance**: Optimized for speed and efficiency
- **Documentation**: Thorough inline and external docs

---

**Technical Specifications Document**  
**Version**: 1.0  
**Last Updated**: June 13, 2025  
**Developed with**: GitHub Copilot AI Assistance  
**Status**: Production Ready
