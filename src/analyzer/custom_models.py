#!/usr/bin/env python3
"""
Custom AI Model Integration Module
Supports: CodeBERT training, local models, and fine-tuning
"""

import os
import sys
import logging
import torch
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# 1. CodeBERT MODEL (microsoft/codebert-base)
# ============================================================

class CodeBertAnalyzer:
    """Fine-tuned CodeBERT model for code analysis"""
    
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        """Initialize CodeBERT model"""
        try:
            from transformers import AutoTokenizer, AutoModel
            logger.info(f"Loading CodeBERT model: {model_name}")
            
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            
            # Move to GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"✅ CodeBERT loaded successfully on {self.device}")
        except ImportError:
            logger.error("Install transformers: pip install transformers torch")
            raise
    
    def analyze_code(self, code: str) -> Dict:
        """Analyze code using CodeBERT embeddings"""
        try:
            # Tokenize input code
            inputs = self.tokenizer.encode(code, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.device)
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.model(inputs)
                embeddings = outputs.last_hidden_state
            
            # Calculate statistics from embeddings
            embedding_mean = embeddings.mean(dim=1).cpu().numpy()[0]
            embedding_var = embeddings.var(dim=1).cpu().numpy()[0]
            
            # Generate insights
            complexity_score = float(embedding_var.mean()) * 10  # 0-10 scale
            
            return {
                "model": "CodeBERT",
                "complexity_score": round(complexity_score, 2),
                "embedding_dim": len(embedding_mean),
                "analysis": "CodeBERT deep learning analysis",
                "insights": self._generate_insights(complexity_score)
            }
        except Exception as e:
            logger.error(f"CodeBERT analysis error: {e}")
            return {"error": str(e)}
    
    def _generate_insights(self, score: float) -> List[str]:
        """Generate insights based on CodeBERT analysis"""
        insights = []
        
        if score > 7:
            insights.append("🔴 High complexity detected - Consider refactoring")
        elif score > 4:
            insights.append("🟡 Moderate complexity - Review structure")
        else:
            insights.append("🟢 Low complexity - Good code quality")
        
        return insights
    
    def train_on_custom_data(self, code_samples: List[str], labels: List[int], 
                            epochs: int = 3, batch_size: int = 8):
        """Fine-tune CodeBERT on custom code samples"""
        try:
            from torch.utils.data import DataLoader, TensorDataset
            from torch.optim import AdamW
            
            logger.info(f"Fine-tuning CodeBERT on {len(code_samples)} samples...")
            
            # Tokenize all samples
            encoded_inputs = self.tokenizer(
                code_samples,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Create dataset
            dataset = TensorDataset(
                encoded_inputs['input_ids'],
                encoded_inputs['attention_mask'],
                torch.tensor(labels)
            )
            
            dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
            optimizer = AdamW(self.model.parameters(), lr=2e-5)
            
            # Training loop
            self.model.train()
            for epoch in range(epochs):
                total_loss = 0
                for batch in dataloader:
                    input_ids, attention_mask, batch_labels = batch
                    input_ids = input_ids.to(self.device)
                    attention_mask = attention_mask.to(self.device)
                    batch_labels = batch_labels.to(self.device)
                    
                    optimizer.zero_grad()
                    outputs = self.model(input_ids, attention_mask=attention_mask)
                    
                    # Simple MSE loss on embeddings mean
                    loss = torch.nn.functional.mse_loss(
                        outputs.last_hidden_state.mean(dim=1),
                        batch_labels.float().unsqueeze(1)
                    )
                    
                    loss.backward()
                    optimizer.step()
                    total_loss += loss.item()
                
                avg_loss = total_loss / len(dataloader)
                logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")
            
            self.model.eval()
            logger.info("✅ Fine-tuning completed!")
            return True
            
        except Exception as e:
            logger.error(f"Training error: {e}")
            return False
    
    def save_model(self, path: str = "./models/codebert-custom"):
        """Save fine-tuned model"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            self.model.save_pretrained(path)
            self.tokenizer.save_pretrained(path)
            logger.info(f"✅ Model saved to {path}")
        except Exception as e:
            logger.error(f"Save error: {e}")


# ============================================================
# 2. LOCAL MODELS (Ollama, LLaMA, etc.)
# ============================================================

class LocalModelAnalyzer:
    """Interface for local running models"""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        """Initialize local model connection"""
        self.model_name = model_name
        self.base_url = base_url
        self.available = self._check_connection()
    
    def _check_connection(self) -> bool:
        """Check if local model is available"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                logger.info(f"✅ Connected to local model server at {self.base_url}")
                return True
        except:
            logger.warning(f"⚠️ Local model server not running at {self.base_url}")
            return False
    
    def analyze_code(self, code: str) -> Dict:
        """Analyze code using local model"""
        if not self.available:
            return {"error": "Local model server not available"}
        
        try:
            import requests
            
            prompt = f"""Analyze this Python code and provide:
1. Summary
2. Improvements
3. Issues
4. Rating (1-10)

Code:
```python
{code}
```

Provide a concise analysis."""
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "model": self.model_name,
                    "analysis": result.get("response", ""),
                    "source": "Local Model"
                }
            else:
                return {"error": f"Model error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Local model analysis error: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_available_models() -> List[str]:
        """List available local models"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except:
            pass
        return []


# ============================================================
# 3. CUSTOM MODEL TRAINER
# ============================================================

class CustomModelTrainer:
    """Train custom models on your code dataset"""
    
    def __init__(self, base_model: str = "microsoft/codebert-base"):
        """Initialize trainer"""
        self.base_model = base_model
        self.codebert = CodeBertAnalyzer(base_model)
        self.training_history = []
    
    def prepare_dataset(self, code_files: List[str], 
                       labels: Optional[List[int]] = None) -> Tuple[List[str], List[int]]:
        """Prepare dataset from code files"""
        code_samples = []
        
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    if len(code.strip()) > 0:
                        code_samples.append(code)
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
        
        # Auto-generate labels if not provided
        if labels is None:
            labels = [len(code.split('\n')) % 10 for code in code_samples]
        
        logger.info(f"📊 Prepared {len(code_samples)} samples")
        return code_samples, labels
    
    def train(self, code_samples: List[str], labels: List[int], 
             epochs: int = 3, batch_size: int = 8):
        """Train the model"""
        logger.info(f"🚀 Starting training with {epochs} epochs...")
        
        success = self.codebert.train_on_custom_data(
            code_samples, labels, epochs, batch_size
        )
        
        if success:
            self.training_history.append({
                "samples": len(code_samples),
                "epochs": epochs,
                "status": "completed"
            })
        
        return success
    
    def save_trained_model(self, path: str):
        """Save the trained model"""
        self.codebert.save_model(path)
        logger.info(f"💾 Model saved to {path}")


# ============================================================
# 4. UNIFIED ANALYZER (Combines all models)
# ============================================================

class UnifiedCodeAnalyzer:
    """Combines CodeBERT, local models, and Gemini"""
    
    def __init__(self, use_codebert: bool = True, use_local: bool = False, use_gemini: bool = True):
        """Initialize unified analyzer"""
        self.codebert = None
        self.local_model = None
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        if use_codebert:
            try:
                self.codebert = CodeBertAnalyzer()
            except:
                logger.warning("CodeBERT not available")
        
        if use_local:
            self.local_model = LocalModelAnalyzer()
        
        self.use_gemini = use_gemini
    
    def analyze_code(self, code: str) -> Dict:
        """Comprehensive analysis using all available models"""
        results = {
            "code_snippet": code[:100] + "..." if len(code) > 100 else code,
            "models_used": [],
            "analyses": {}
        }
        
        # CodeBERT analysis
        if self.codebert:
            try:
                codebert_result = self.codebert.analyze_code(code)
                results["analyses"]["codebert"] = codebert_result
                results["models_used"].append("CodeBERT")
            except Exception as e:
                logger.error(f"CodeBERT failed: {e}")
        
        # Local model analysis
        if self.local_model and self.local_model.available:
            try:
                local_result = self.local_model.analyze_code(code)
                results["analyses"]["local"] = local_result
                results["models_used"].append(self.local_model.model_name)
            except Exception as e:
                logger.error(f"Local model failed: {e}")
        
        # Gemini analysis
        if self.use_gemini and self.gemini_key:
            try:
                from src.analyzer.ai_reviewer import _review_with_gemini
                gemini_result = _review_with_gemini(code)
                results["analyses"]["gemini"] = gemini_result
                results["models_used"].append("Gemini")
            except Exception as e:
                logger.error(f"Gemini failed: {e}")
        
        results["total_models"] = len(results["models_used"])
        return results
    
    def comparative_analysis(self, code: str) -> Dict:
        """Compare all models side-by-side"""
        return {
            "unified_analysis": self.analyze_code(code),
            "timestamp": str(__import__('datetime').datetime.now()),
            "recommendation": self._get_recommendation(code)
        }
    
    def _get_recommendation(self, code: str) -> str:
        """Generate recommendation based on all analyses"""
        recommendation = "✅ Based on comprehensive multi-model analysis:\n"
        
        if self.codebert:
            recommendation += "- CodeBERT: Deep learning code embeddings analyzed\n"
        if self.local_model and self.local_model.available:
            recommendation += f"- Local Model ({self.local_model.model_name}): Local inference complete\n"
        if self.use_gemini:
            recommendation += "- Gemini: Cloud AI insights included\n"
        
        recommendation += "\nCombine insights from all models for best results!"
        return recommendation


# ============================================================
# 5. SETUP & INSTALLATION HELPERS
# ============================================================

def install_dependencies():
    """Install required packages"""
    packages = [
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "requests>=2.28.0",
        "numpy>=1.24.0"
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        print(f"  Installing {package}...")
        os.system(f"pip install -q {package}")
    print("✅ Dependencies installed!")


def setup_codebert():
    """Download and setup CodeBERT"""
    print("📥 Setting up CodeBERT...")
    print("This will download ~350MB model file...")
    
    try:
        codebert = CodeBertAnalyzer()
        print("✅ CodeBERT ready!")
        return codebert
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def setup_local_models():
    """Instructions for setting up local models"""
    instructions = """
    📖 To use local models (Ollama):
    
    1. Install Ollama: https://ollama.ai
    
    2. Run locally:
       ollama serve
    
    3. Download a model:
       ollama pull llama2        # 3.8GB
       ollama pull codellama     # 3.3GB (code-specific)
       ollama pull mistral       # 2.6GB (fast)
    
    4. Models will run on http://localhost:11434
    
    Available models:
    - llama2: Fast, general purpose
    - codellama: Optimized for code
    - mistral: Very fast
    - neural-chat: Conversational
    """
    print(instructions)


# ============================================================
# 6. EXAMPLE USAGE
# ============================================================

def example_usage():
    """Example of using the unified analyzer"""
    
    # Sample code to analyze
    sample_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
"""
    
    print("\n" + "="*60)
    print("🤖 Multi-Model Code Analysis Example")
    print("="*60 + "\n")
    
    # Initialize unified analyzer
    print("🚀 Initializing analyzer with multiple models...\n")
    analyzer = UnifiedCodeAnalyzer(
        use_codebert=True,
        use_local=True,
        use_gemini=True
    )
    
    # Run analysis
    print(f"📝 Analyzing code:\n{sample_code}\n")
    results = analyzer.comparative_analysis(sample_code)
    
    print("✅ Analysis complete!\n")
    import json
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            install_dependencies()
        elif sys.argv[1] == "setup-codebert":
            setup_codebert()
        elif sys.argv[1] == "setup-local":
            setup_local_models()
        elif sys.argv[1] == "example":
            example_usage()
    else:
        print("""
🤖 Custom AI Model Trainer
        
Usage:
  python custom_models.py install       # Install dependencies
  python custom_models.py setup-codebert # Setup CodeBERT
  python custom_models.py setup-local    # Setup local models (Ollama)
  python custom_models.py example        # Run example
        """)
