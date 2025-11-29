# 🤖 Custom Model Training & Integration Guide

Complete guide for training **CodeBERT**, running **local models**, and using **custom models** in your code analyzer.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [CodeBERT Training](#codebert-training)
3. [Local Models (Ollama)](#local-models-ollama)
4. [Unified Multi-Model Analysis](#unified-multi-model-analysis)
5. [Integration with Flask](#integration-with-flask)
6. [Examples](#examples)

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Navigate to project directory
cd /home/dev-trivedi/Public/Projects/AI/code_analyst

# Install required packages
python3 src/analyzer/custom_models.py install
```

### 2. Setup CodeBERT

```bash
# Download and setup CodeBERT (first run ~2-3 minutes)
python3 src/analyzer/custom_models.py setup-codebert

# Or run example
python3 src/analyzer/custom_models.py example
```

### 3. Setup Local Models (Optional)

```bash
# Get instructions for Ollama setup
python3 src/analyzer/custom_models.py setup-local
```

---

## 🧠 CodeBERT Training

### What is CodeBERT?

**CodeBERT** (`microsoft/codebert-base`) is a pre-trained transformer model for code understanding:

- 12 transformer layers
- 768 hidden dimensions
- Trained on 6+ million GitHub repositories
- State-of-the-art for code embeddings and analysis

### Training on Your Code

```python
from src.analyzer.custom_models import CustomModelTrainer

# Initialize trainer
trainer = CustomModelTrainer(base_model="microsoft/codebert-base")

# Your code samples
code_samples = [
    """
    def add(a, b):
        return a + b
    """,
    """
    def calculate_total(items):
        total = 0
        for item in items:
            total += item['price']
        return total
    """
]

# Labels (0-10 complexity score, auto-generated if not provided)
labels = [1, 5]  # Optional - auto-generated if omitted

# Train the model
trainer.train(
    code_samples=code_samples,
    labels=labels,
    epochs=3,           # Number of training passes
    batch_size=8        # Samples per batch
)

# Save trained model
trainer.save_trained_model("./models/my-codebert")
```

### Training on Local Files

```python
from pathlib import Path

# Get all Python files
code_files = list(Path("src").glob("**/*.py"))

# Prepare dataset
code_samples, labels = trainer.prepare_dataset(code_files)

# Train
trainer.train(code_samples, labels, epochs=5)

# Save
trainer.save_trained_model("./models/codebert-trained")
```

### Advanced Training Configuration

```python
# GPU training (automatic if available)
import torch
print(f"Using: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")

# Training with different parameters
trainer.train(
    code_samples=code_samples,
    labels=labels,
    epochs=10,          # More epochs = better fitting (but longer)
    batch_size=16       # Larger batch = better memory usage
)

# Load and use trained model
from src.analyzer.custom_models import CodeBertAnalyzer
codebert = CodeBertAnalyzer("./models/codebert-trained")
result = codebert.analyze_code("def hello(): pass")
print(result)
```

---

## 🏠 Local Models (Ollama)

### What is Ollama?

**Ollama** lets you run large language models locally:

- No cloud dependency
- Complete privacy
- Supports: LLaMA, CodeLLaMA, Mistral, etc.
- Fast local inference

### Setup Ollama

#### 1. Install Ollama

**macOS/Linux:**

```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**

- Download from https://ollama.ai

#### 2. Start Ollama Server

```bash
ollama serve
# Server runs on http://localhost:11434
```

#### 3. Download a Model

```bash
# In another terminal:

# CodeLLaMA - BEST for code (3.3GB)
ollama pull codellama

# LLaMA 2 - General purpose (3.8GB)
ollama pull llama2

# Mistral - Fast and efficient (2.6GB)
ollama pull mistral

# Neural Chat - Conversational (4.1GB)
ollama pull neural-chat
```

### Using Local Models

```python
from src.analyzer.custom_models import LocalModelAnalyzer

# Initialize with model name
analyzer = LocalModelAnalyzer(model_name="codellama")

# Analyze code
code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

result = analyzer.analyze_code(code)
print(result)

# Output:
# {
#     "model": "codellama",
#     "analysis": "This recursive function implements Fibonacci...",
#     "source": "Local Model"
# }
```

### List Available Models

```python
models = LocalModelAnalyzer.get_available_models()
print(models)  # ['codellama', 'llama2', 'mistral']
```

### Model Comparison

| Model           | Size  | Speed  | Best For                      |
| --------------- | ----- | ------ | ----------------------------- |
| **CodeLLaMA**   | 3.3GB | Medium | Code analysis (RECOMMENDED)   |
| **Mistral**     | 2.6GB | Fast   | Quick analysis, low resources |
| **LLaMA 2**     | 3.8GB | Medium | General purpose               |
| **Neural Chat** | 4.1GB | Slow   | Detailed explanations         |

---

## 🔀 Unified Multi-Model Analysis

### Combine All Models

```python
from src.analyzer.custom_models import UnifiedCodeAnalyzer

# Initialize with all available models
analyzer = UnifiedCodeAnalyzer(
    use_codebert=True,    # CodeBERT embeddings
    use_local=True,       # Local model (Ollama)
    use_gemini=True       # Gemini API
)

code = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""

# Get comprehensive analysis
analysis = analyzer.comparative_analysis(code)
```

### Output Format

```json
{
  "unified_analysis": {
    "code_snippet": "def process_data(data):",
    "models_used": ["CodeBERT", "codellama", "Gemini"],
    "analyses": {
      "codebert": {
        "model": "CodeBERT",
        "complexity_score": 3.45,
        "embedding_dim": 768,
        "insights": ["🟢 Low complexity - Good code quality"]
      },
      "local": {
        "model": "codellama",
        "analysis": "The function processes a list of items...",
        "source": "Local Model"
      },
      "gemini": {
        "model": "Gemini",
        "summary": "...",
        "suggestions": [...],
        "rating": 8.5
      }
    },
    "total_models": 3
  },
  "recommendation": "✅ Based on comprehensive multi-model analysis..."
}
```

---

## 🚀 Integration with Flask

### Update Flask App

Add custom models to your analyzer:

```python
# In src/app.py, add this import
from src.analyzer.model_integration import get_custom_model_integration

# In your Flask route
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data.get('code')
    model = data.get('model', 'unified')  # New: specify model

    # Try custom models first
    integration = get_custom_model_integration()

    if model in ['codebert', 'local', 'unified']:
        result = integration.analyze_with_model(code, model)
        if result['status'] == 'success':
            return jsonify(result)

    # Fallback to existing analyzers
    # ... existing code ...
```

### API Endpoints

#### Use CodeBERT

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a,b): return a+b",
    "model": "codebert"
  }'
```

#### Use Local Model

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a,b): return a+b",
    "model": "local"
  }'
```

#### Use Unified Analysis

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a,b): return a+b",
    "model": "unified"
  }'
```

---

## 📝 Examples

### Example 1: Train CodeBERT on Your Project

```python
from src.analyzer.custom_models import CustomModelTrainer
from pathlib import Path

# 1. Collect all Python files
trainer = CustomModelTrainer()
code_files = list(Path("src").glob("**/*.py"))

# 2. Prepare dataset
samples, labels = trainer.prepare_dataset(code_files)
print(f"Training on {len(samples)} files")

# 3. Train
trainer.train(samples, labels, epochs=5, batch_size=16)

# 4. Save
trainer.save_trained_model("./models/project-codebert")

# 5. Use it
from src.analyzer.custom_models import CodeBertAnalyzer
model = CodeBertAnalyzer("./models/project-codebert")
result = model.analyze_code("def my_func(): pass")
print(result)
```

### Example 2: Compare All Models on Same Code

```python
from src.analyzer.custom_models import UnifiedCodeAnalyzer
import json

analyzer = UnifiedCodeAnalyzer(
    use_codebert=True,
    use_local=True,
    use_gemini=True
)

test_code = """
class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        results = []
        for item in self.data:
            if item > 0:
                results.append(item * 2)
        return results
"""

# Get analysis from all models
analysis = analyzer.comparative_analysis(test_code)

# Pretty print results
print(json.dumps(analysis, indent=2, default=str))
```

### Example 3: Continuous Training Pipeline

```python
from src.analyzer.custom_models import CustomModelTrainer
from pathlib import Path
import time

trainer = CustomModelTrainer()

# Training loop - continuously improve model
for iteration in range(3):
    print(f"\n📈 Iteration {iteration + 1}/3")

    # Get latest code files
    code_files = list(Path("src").glob("**/*.py"))
    samples, labels = trainer.prepare_dataset(code_files)

    # Train with increasing epochs
    epochs = (iteration + 1) * 3
    trainer.train(samples, labels, epochs=epochs, batch_size=8)

    # Save version
    trainer.save_trained_model(f"./models/codebert-v{iteration+1}")

    time.sleep(5)

print("✅ Training pipeline complete!")
```

---

## 🔧 Troubleshooting

### CodeBERT Memory Error

```bash
# Use CPU if CUDA memory is limited
export CUDA_VISIBLE_DEVICES=""  # Disable GPU
python3 script.py
```

### Local Model Connection Error

```bash
# Ensure Ollama is running
ollama serve

# In another terminal, verify:
curl http://localhost:11434/api/tags
```

### Slow Training

```python
# Reduce batch size for GPU memory issues
trainer.train(samples, labels, batch_size=4, epochs=2)

# Or run on GPU explicitly
import torch
print(torch.cuda.is_available())  # Should be True
```

---

## 📊 Performance Metrics

| Model            | Latency   | Accuracy  | Memory      | Best Use      |
| ---------------- | --------- | --------- | ----------- | ------------- |
| **CodeBERT**     | 100-500ms | High      | 2GB         | Deep analysis |
| **Local (Fast)** | 1-5s      | Medium    | 4-6GB       | Real-time     |
| **Gemini**       | 2-5s      | Very High | 0MB (cloud) | Complex code  |
| **Unified**      | 5-10s     | Highest   | Combined    | Production    |

---

## 🎯 Next Steps

1. **Install dependencies**: `python3 src/analyzer/custom_models.py install`
2. **Setup CodeBERT**: `python3 src/analyzer/custom_models.py setup-codebert`
3. **Setup Ollama** (optional): Install from https://ollama.ai
4. **Run example**: `python3 src/analyzer/custom_models.py example`
5. **Integrate with Flask**: Update `src/app.py` with model integration
6. **Train on your data**: Use `CustomModelTrainer` with your code
7. **Deploy**: Push to production with your trained models

---

## 📚 Resources

- **CodeBERT Paper**: https://arxiv.org/abs/2002.08155
- **Ollama**: https://ollama.ai
- **Hugging Face Models**: https://huggingface.co/microsoft/codebert-base
- **Transformers Library**: https://huggingface.co/docs/transformers

---

## ❓ Questions?

Check the example usage:

```bash
python3 src/analyzer/custom_models.py example
```

Or integrate into Flask:

```python
from src.analyzer.model_integration import get_custom_model_integration
integration = get_custom_model_integration()
print(integration.get_available_models())
```

---

**Happy coding! 🚀**
