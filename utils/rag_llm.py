# filepath: c:\Users\aksha\OneDrive\Desktop\jivabot\utils\rag_llm.py
import os
from typing import List, Dict, Any
import json
import requests
import time
from functools import wraps

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

class RAGLLM:
    def __init__(self, api_key: str):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = api_key

    def build_prompt(self, query: str, context_chunks: List[str]) -> List[Dict[str, str]]:
        """Build a RAG prompt with context."""
        context = "\n\n".join(context_chunks)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant for Jiva Infotech. Answer questions based on the provided context. "
                          "If you cannot find the answer in the context, say so politely."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
        return messages

    @retry_with_backoff(retries=3, backoff_in_seconds=1)
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenRouter API with retry logic."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jivabot.streamlit.app",
            "X-Title": "JivaBot"
        }
        
        data = {
            "model": "mistralai/mixtral-8x7b-instruct",
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 402:
                raise Exception("API key has insufficient credits or payment is required. Please check your OpenRouter account.")
            elif response.status_code == 401:
                raise Exception("Invalid API key. Please check your OpenRouter API key configuration.")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again in a moment.")
            elif response.status_code >= 400:
                error_msg = f"API Error {response.status_code}: {response.text}"
                raise Exception(error_msg)
            
            response.raise_for_status()
            
            result = response.json()
            if "choices" not in result or not result["choices"]:
                raise Exception("Invalid response format from API")
                
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.Timeout:
            raise Exception("API request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to API. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def generate_response(self, query: str, context_chunks: List[str]) -> str:
        """Generate a response using RAG."""
        messages = self.build_prompt(query, context_chunks)
        return self.get_response(messages)

if __name__ == "__main__":
    # Test the module
    import os
    test_api_key = os.getenv("OPENROUTER_API_KEY", "test-key")
    rag = RAGLLM(test_api_key)
    
    # Example usage
    test_chunks = ["Jiva Infotech is a leading technology company."]
    response = rag.generate_response("What is Jiva Infotech?", test_chunks)
    print(f"Response: {response}")
