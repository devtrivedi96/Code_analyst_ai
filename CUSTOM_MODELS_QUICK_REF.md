# 🎯 Quick Reference: Custom Models

## 📦 One-Time Setup

```bash
# Install dependencies (5 minutes)
python3 src/analyzer/custom_models.py install

# Download CodeBERT (first run downloads ~350MB)
python3 src/analyzer/custom_models.py setup-codebert
```

---

## 🚀 Quick Commands

### Train on Your Project

```bash
python3 train_models.py train-project
# Trains CodeBERT on all Python files in current directory
```

### Train on Specific Folder

```bash
python3 train_models.py train-project src ./models/my-model
```

### Create Dataset

```bash
python3 train_models.py create-dataset src code_samples.json
```

### Train on Dataset

```bash
python3 train_models.py train-dataset code_samples.json
```

### Compare Models

```bash
python3 train_models.py compare "def add(a,b): return a+b"
```

### Benchmark Models

```bash
python3 train_models.py benchmark
```

---

## 🐍 Python Usage

### CodeBERT Only

```python
from src.analyzer.custom_models import CodeBertAnalyzer

model = CodeBertAnalyzer()
result = model.analyze_code("def hello(): pass")
print(result)
# Output: {'model': 'CodeBERT', 'complexity_score': 1.23, ...}
```

### Local Model (Ollama)

```python
from src.analyzer.custom_models import LocalModelAnalyzer

# First: Start ollama in another terminal
# ollama serve

analyzer = LocalModelAnalyzer(model_name="codellama")
result = analyzer.analyze_code("def hello(): pass")
print(result['analysis'])
```

### Unified Analysis (All Models)

```python
from src.analyzer.custom_models import UnifiedCodeAnalyzer

analyzer = UnifiedCodeAnalyzer(
    use_codebert=True,
    use_local=True,
    use_gemini=True
)

result = analyzer.comparative_analysis("def hello(): pass")
print(result)
```

### Train CodeBERT

```python
from src.analyzer.custom_models import CustomModelTrainer

trainer = CustomModelTrainer()
trainer.train(
    code_samples=["def add(a,b): return a+b", "def mul(a,b): return a*b"],
    labels=[1, 1],
    epochs=3
)
trainer.save_trained_model("./models/my-model")
```

---

## 🔧 Setup Local Models (Ollama)

### 1. Install Ollama

```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh

# Then start:
ollama serve
```

### 2. Download Model

```bash
# In another terminal:
ollama pull codellama    # Code-specific (RECOMMENDED)
ollama pull mistral      # Fast
ollama pull llama2       # General purpose
```

### 3. Use in Code

```python
from src.analyzer.custom_models import LocalModelAnalyzer
analyzer = LocalModelAnalyzer(model_name="codellama")
result = analyzer.analyze_code(your_code)
```

---

## 📊 Model Comparison

| Feature  | CodeBERT         | Local Model   | Gemini        | Unified      |
| -------- | ---------------- | ------------- | ------------- | ------------ |
| Setup    | Easy             | Medium        | Easy          | Combined     |
| Speed    | Fast (100-500ms) | Medium (1-5s) | Medium (2-5s) | Slow (5-10s) |
| Accuracy | Good             | Very Good     | Excellent     | Best         |
| Privacy  | Local            | Local         | Cloud         | Mixed        |
| Cost     | Free             | Free          | Free tier     | Depends      |

---

## 🎓 Training Examples

### Simple Training

```python
trainer = CustomModelTrainer()
trainer.train(
    code_samples=["def x(): pass"],
    epochs=1
)
```

### Training on Files

```python
from pathlib import Path
files = list(Path("src").glob("**/*.py"))
samples, labels = trainer.prepare_dataset(files)
trainer.train(samples, labels, epochs=5)
```

### Continuous Improvement

```python
for i in range(3):
    trainer.train(samples, labels, epochs=3)
    trainer.save_trained_model(f"./models/v{i+1}")
```

---

## 🐛 Troubleshooting

| Problem                        | Solution                                  |
| ------------------------------ | ----------------------------------------- |
| `No module named transformers` | `pip install transformers torch`          |
| Memory error on CodeBERT       | Use CPU: `export CUDA_VISIBLE_DEVICES=""` |
| Local model connection fails   | Start Ollama: `ollama serve`              |
| Gemini key error               | Set: `export GEMINI_API_KEY="your-key"`   |
| Slow on first run              | First run downloads ~2GB - be patient!    |

---

## 📁 File Structure

```
code_analyst/
├── src/analyzer/
│   ├── custom_models.py           # Main module
│   └── model_integration.py        # Flask integration
├── CUSTOM_MODELS_GUIDE.md          # Full guide
├── train_models.py                 # CLI tool
└── models/                         # Your trained models
    ├── codebert-custom/            # Custom trained
    ├── my-model/                   # Your model
    └── v1/, v2/, etc.              # Model versions
```

---

## ✅ Common Tasks

### Train CodeBERT on Entire Project

```bash
python3 train_models.py train-project . ./models/project-codebert
```

### Use Your Trained Model

```python
from src.analyzer.custom_models import CodeBertAnalyzer
model = CodeBertAnalyzer("./models/project-codebert")
result = model.analyze_code(code)
```

### Add to Flask API

```python
from src.analyzer.model_integration import get_custom_model_integration
integration = get_custom_model_integration()
result = integration.analyze_with_model(code, "codebert")
```

### Compare All Models

```bash
python3 train_models.py compare "def fib(n): return n if n<2 else fib(n-1)+fib(n-2)"
```

---

## 📚 Learn More

- **Full Guide**: See `CUSTOM_MODELS_GUIDE.md`
- **Examples**: `python3 src/analyzer/custom_models.py example`
- **Help**: `python3 train_models.py help`

---

## 🎯 Next Steps

1. ✅ Run setup: `python3 src/analyzer/custom_models.py install`
2. ✅ Train: `python3 train_models.py train-project`
3. ✅ Compare: `python3 train_models.py compare "your code"`
4. ✅ Integrate: Add to Flask with `model_integration.py`
5. ✅ Deploy: Use trained models in production

---

**Happy training! 🚀**
