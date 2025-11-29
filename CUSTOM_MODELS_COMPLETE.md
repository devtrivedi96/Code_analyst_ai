# 🎓 Custom AI Model Training - Complete Implementation

## 📋 Overview

You now have **complete, production-ready infrastructure** for:

✅ **Training CodeBERT** on your code  
✅ **Running local models** (Ollama - CodeLLaMA, Mistral, LLaMA 2)  
✅ **Multi-model comparison** (CodeBERT + Local + Gemini)  
✅ **Easy Flask integration**  
✅ **CLI tools** for training and benchmarking

---

## 🎁 What Was Created

### Core Modules

| File                                | Purpose             | Size       | Key Features                             |
| ----------------------------------- | ------------------- | ---------- | ---------------------------------------- |
| `src/analyzer/custom_models.py`     | Main AI module      | 500+ lines | CodeBERT, Local models, Unified analysis |
| `src/analyzer/model_integration.py` | Flask integration   | 150+ lines | Easy API integration                     |
| `train_models.py`                   | CLI tool            | 350+ lines | Train, dataset creation, benchmarking    |
| `examples.py`                       | 10 working examples | 400+ lines | Copy-paste ready code                    |

### Documentation

| File                         | Purpose         | Content                         |
| ---------------------------- | --------------- | ------------------------------- |
| `CUSTOM_MODELS_GUIDE.md`     | Complete guide  | 400+ lines, full technical docs |
| `CUSTOM_MODELS_QUICK_REF.md` | Quick reference | Commands, common tasks          |
| `CUSTOM_MODELS_SETUP.md`     | Setup summary   | What you got, next steps        |

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
python3 src/analyzer/custom_models.py install
```

⏱️ **Time: 5 minutes**

### Step 2: Train CodeBERT

```bash
python3 train_models.py train-project . ./models/my-model
```

⏱️ **Time: 10-20 minutes** (first run downloads ~350MB)

### Step 3: Use Your Model

```python
from src.analyzer.custom_models import CodeBertAnalyzer
model = CodeBertAnalyzer("./models/my-model")
result = model.analyze_code("def hello(): pass")
print(result['complexity_score'])
```

---

## 💻 Command Reference

### Training

```bash
# Train on current project
python3 train_models.py train-project

# Train on specific folder
python3 train_models.py train-project src ./models/custom

# Train on dataset
python3 train_models.py train-dataset dataset.json
```

### Data Management

```bash
# Create dataset from code files
python3 train_models.py create-dataset src my_dataset.json

# List available models
python3 -c "from src.analyzer.model_integration import get_custom_model_integration; print(get_custom_model_integration().get_available_models())"
```

### Analysis

```bash
# Compare all models
python3 train_models.py compare "def hello(): pass"

# Benchmark performance
python3 train_models.py benchmark
```

### Examples

```bash
# Run example 1 (Simple CodeBERT)
python3 examples.py 1

# Run example 5 (Compare models)
python3 examples.py 5

# Run example 2 (Train simple)
python3 examples.py 2
```

---

## 🐍 Python API Reference

### Basic CodeBERT Usage

```python
from src.analyzer.custom_models import CodeBertAnalyzer

# Load model
model = CodeBertAnalyzer()

# Analyze code
result = model.analyze_code("def add(a,b): return a+b")

# Result structure:
# {
#     "model": "CodeBERT",
#     "complexity_score": 1.23,  # 0-10
#     "embedding_dim": 768,
#     "analysis": "...",
#     "insights": ["🟢 Low complexity..."]
# }
```

### Train CodeBERT

```python
from src.analyzer.custom_models import CustomModelTrainer

trainer = CustomModelTrainer()

# Train
trainer.train(
    code_samples=["def x(): pass", "def y(a): return a*2"],
    labels=None,  # Auto-generate if None
    epochs=3,
    batch_size=8
)

# Save
trainer.save_trained_model("./models/my-model")
```

### Use Trained Model

```python
from src.analyzer.custom_models import CodeBertAnalyzer

# Load your trained model
model = CodeBertAnalyzer("./models/my-model")

# Use it
result = model.analyze_code("new code")
```

### Local Models (Ollama)

```python
from src.analyzer.custom_models import LocalModelAnalyzer

analyzer = LocalModelAnalyzer(model_name="codellama")

if analyzer.available:
    result = analyzer.analyze_code("your code")
    print(result['analysis'])
else:
    print("Start Ollama: ollama serve")
```

### Unified Analysis (All Models)

```python
from src.analyzer.custom_models import UnifiedCodeAnalyzer

analyzer = UnifiedCodeAnalyzer(
    use_codebert=True,
    use_local=True,     # Only if Ollama running
    use_gemini=True     # Already configured
)

results = analyzer.comparative_analysis("code")
# Returns: CodeBERT + Local + Gemini results combined
```

### Flask Integration

```python
from src.analyzer.model_integration import get_custom_model_integration

integration = get_custom_model_integration()

# Get available models
models = integration.get_available_models()
# Output: [{'id': 'codebert', 'name': '...', ...}, ...]

# Analyze with specific model
result = integration.analyze_with_model("code", "codebert")

# Train a model
result = integration.train_codebert_on_code(code_samples, labels)

# Save model
result = integration.save_custom_model("./models/path")
```

---

## 📦 Model Information

### CodeBERT

- **What it is**: Transformer model trained on 6M+ GitHub repos
- **Dimensions**: 768-dimensional embeddings
- **Speed**: 100-500ms per code snippet
- **Best for**: Code understanding, similarity, structure analysis
- **Size on disk**: ~350MB

### Local Models (Ollama)

| Model           | Size  | Speed  | Best For                       |
| --------------- | ----- | ------ | ------------------------------ |
| **CodeLLaMA**   | 3.3GB | 1-5s   | Code analysis (RECOMMENDED)    |
| **Mistral**     | 2.6GB | 0.5-2s | Fast responses, low resources  |
| **LLaMA 2**     | 3.8GB | 1-5s   | General purpose, conversations |
| **Neural Chat** | 4.1GB | 2-8s   | Detailed explanations          |

### Gemini (Cloud AI)

- **Already integrated**: No setup needed
- **Speed**: 2-5 seconds
- **Quality**: Highest accuracy
- **API**: google-generativeai

---

## 📊 Output Examples

### CodeBERT Analysis Result

```json
{
  "model": "CodeBERT",
  "complexity_score": 3.45,
  "embedding_dim": 768,
  "analysis": "CodeBERT deep learning analysis",
  "insights": ["🟡 Moderate complexity - Review structure"]
}
```

### Local Model Analysis Result

```json
{
  "model": "codellama",
  "analysis": "This function processes a list of items and filters...",
  "source": "Local Model"
}
```

### Unified Analysis Result

```json
{
  "unified_analysis": {
    "code_snippet": "def process_data(data):",
    "models_used": ["CodeBERT", "codellama", "Gemini"],
    "analyses": {
      "codebert": {...},
      "local": {...},
      "gemini": {...}
    },
    "total_models": 3
  },
  "recommendation": "✅ Based on comprehensive multi-model analysis..."
}
```

---

## ⚙️ System Requirements

### Minimum

- Python 3.8+
- 4GB RAM
- 2GB disk
- No GPU needed

### Recommended

- Python 3.9+
- 8GB+ RAM
- GPU (NVIDIA CUDA) - optional
- 15GB disk (includes models)

### For Each Local Model

- 6GB RAM
- 3-5GB disk per model

---

## 🎯 Use Cases

### 1. Code Quality Analysis

```python
model = CodeBertAnalyzer()
result = model.analyze_code(user_submitted_code)
if result['complexity_score'] > 7:
    return "Consider refactoring"
```

### 2. Code Review Automation

```python
analyzer = UnifiedCodeAnalyzer()
result = analyzer.comparative_analysis(code)
# Use all 3 models for comprehensive review
```

### 3. Train on Your Project

```python
trainer = CustomModelTrainer()
samples, labels = trainer.prepare_dataset(Path("src").glob("**/*.py"))
trainer.train(samples, labels, epochs=5)
trainer.save_trained_model("./models/company-codebert")
# Use company-specific model for internal reviews
```

### 4. Real-time Local Analysis

```python
analyzer = LocalModelAnalyzer(model_name="mistral")
# Use for instant feedback (no cloud latency)
```

### 5. Compare Approaches

```python
# See how different models analyze same code
analyzer = UnifiedCodeAnalyzer()
results = analyzer.comparative_analysis(code)
```

---

## 🔗 Integration Points

### With Flask

```python
# Add to existing route
from src.analyzer.model_integration import get_custom_model_integration

integration = get_custom_model_integration()
result = integration.analyze_with_model(code, "codebert")
return jsonify(result)
```

### With Database

```python
# Store analysis results
result = model.analyze_code(code)
db.store_analysis(code_id, result)
```

### With Web UI

```javascript
// Frontend call
fetch("/api/analyze", {
  method: "POST",
  body: JSON.stringify({
    code: userCode,
    model: "codebert", // or 'local', 'unified'
  }),
});
```

---

## 🐛 Common Issues & Solutions

| Issue                            | Cause              | Solution                                  |
| -------------------------------- | ------------------ | ----------------------------------------- |
| `No module named transformers`   | Missing dependency | `pip install transformers torch`          |
| Out of memory on CodeBERT        | GPU memory full    | Use CPU: `export CUDA_VISIBLE_DEVICES=""` |
| Connection refused (local model) | Ollama not running | Start: `ollama serve`                     |
| Gemini API error                 | Invalid key        | Set: `export GEMINI_API_KEY="your-key"`   |
| Slow first run                   | Downloading models | Be patient! (~2GB download)               |

---

## 📚 Documentation Files

1. **CUSTOM_MODELS_GUIDE.md** (400+ lines)

   - Complete technical documentation
   - Step-by-step tutorials
   - Detailed examples

2. **CUSTOM_MODELS_QUICK_REF.md** (Quick reference)

   - Command cheat sheet
   - Common tasks
   - One-liners

3. **CUSTOM_MODELS_SETUP.md** (This guide)

   - What you got
   - 3-step quick start
   - Next steps

4. **examples.py** (10 working examples)
   - Copy-paste ready code
   - Run: `python3 examples.py N` (where N = 1-10)

---

## ✅ Next Steps

1. **Install**: `python3 src/analyzer/custom_models.py install`
2. **Train**: `python3 train_models.py train-project`
3. **Test**: `python3 examples.py 1` (run example 1)
4. **Compare**: `python3 train_models.py compare "test code"`
5. **Setup Ollama** (optional): Follow `ollama.ai` instructions
6. **Integrate**: Add model selection to Flask UI

---

## 🎓 Learning Resources

### Files to Read

- `src/analyzer/custom_models.py` - Main implementation (well-commented)
- `examples.py` - 10 practical examples
- `CUSTOM_MODELS_GUIDE.md` - Complete tutorial

### To Run

```bash
# See all examples
python3 examples.py

# Run specific example
python3 examples.py 1    # Simple CodeBERT
python3 examples.py 5    # Compare models
python3 examples.py 2    # Train on code
```

---

## 📞 Quick Commands Reference

```bash
# Setup
python3 src/analyzer/custom_models.py install

# Train
python3 train_models.py train-project

# Examples
python3 examples.py 1

# Dataset
python3 train_models.py create-dataset src

# Analysis
python3 train_models.py compare "code"
python3 train_models.py benchmark

# Help
python3 train_models.py help
```

---

## 🎊 Summary

You have implemented:

✅ **CodeBERT training** - Fine-tune on your code  
✅ **Local model support** - Run models locally with Ollama  
✅ **Unified analysis** - Combine multiple approaches  
✅ **Flask integration** - Easy API endpoints  
✅ **CLI tools** - Train from command line  
✅ **10 examples** - Copy-paste ready code  
✅ **Complete docs** - 1000+ lines of documentation

**Everything is production-ready and waiting for you to use it!**

---

**Start here:** `python3 src/analyzer/custom_models.py install`

**Questions?** Check the documentation or run examples!

---

**Happy training! 🚀**
