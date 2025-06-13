"""
Torch utilities for handling watcher issues in Streamlit Cloud.
This module provides a safe way to import and configure torch to prevent file watcher errors.
"""

import os
import warnings

def setup_torch_environment():
    """Set up environment variables to prevent torch watcher issues."""
    os.environ.update({
        "TOKENIZERS_PARALLELISM": "false",
        "TORCH_DISABLE_WATCHDOG": "1",
        "TORCH_JIT_DISABLE_WATCHDOG": "1",
        "STREAMLIT_WATCHER_IGNORE_MODULES": "torch,torch.classes,torch.jit,torch.nn,torch.utils",
        "STREAMLIT_SERVER_RUN_ON_SAVE": "false",
        "PYTHONUNBUFFERED": "1"
    })

def safe_torch_import():
    """Safely import torch with watcher suppression."""
    setup_torch_environment()
    warnings.filterwarnings("ignore")
    
    try:
        import torch
        # Disable JIT logging if available
        if hasattr(torch, 'jit') and hasattr(torch.jit, '_set_jit_logging'):
            torch.jit._set_jit_logging(False)
        
        # Disable file watching in torch
        if hasattr(torch, '_C') and hasattr(torch._C, '_set_print_file_logging'):
            try:
                torch._C._set_print_file_logging(False)
            except:
                pass
                
        return torch
    except ImportError:
        return None

def suppress_all_warnings():
    """Suppress all warnings that might cause issues."""
    warnings.filterwarnings("ignore")
    
    # Suppress specific warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*file_watcher.*")
    warnings.filterwarnings("ignore", message=".*torch.*")

# Initialize on import
setup_torch_environment()
suppress_all_warnings()
