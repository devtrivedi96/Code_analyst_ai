# 🎓 Custom Model Training - Complete Setup Summary

## ✅ What's Been Created

You now have **complete infrastructure** for training and running custom AI models! Here's what was added:

### 📁 New Files Created

1. **`src/analyzer/custom_models.py`** (500+ lines)

   - CodeBERT analyzer with training capabilities
   - Local model support (Ollama)
   - Unified multi-model analysis
   - Complete training pipeline

2. **`src/analyzer/model_integration.py`** (150+ lines)

   - Flask integration layer
   - Model management
   - Easy API endpoint integration

3. **`train_models.py`** (350+ lines)

   - CLI tool for training
   - Dataset creation
   - Model benchmarking
   - Comparison utilities

4. **`CUSTOM_MODELS_GUIDE.md`** (Comprehensive)

   - Full technical documentation
   - Step-by-step tutorials
   - Code examples
   - Troubleshooting

5. **`CUSTOM_MODELS_QUICK_REF.md`** (Quick reference)
   - Commands cheat sheet
   - Common tasks
   - One-liners

---

## 🎯 What You Can Do Now

### 1️⃣ **Train CodeBERT on Your Code**

```bash
python3 train_models.py train-project
```

✓ Automatically collects all Python files  
✓ Trains deep learning model specific to your code  
✓ Saves fine-tuned model  
✓ Takes ~10-15 minutes

### 2️⃣ **Run Local Models (Ollama)**

```bash
# In terminal 1:
ollama serve

# In terminal 2:
python3 train_models.py compare "your code"
```

✓ Run AI models locally (no cloud needed)  
✓ Private, fast inference  
✓ Support for CodeLLaMA, LLaMA 2, Mistral, etc.

### 3️⃣ **Compare All Models Side-by-Side**

```bash
python3 train_models.py compare "def hello(): pass"
```

✓ See results from CodeBERT + Local + Gemini  
✓ Understand strengths of each model  
✓ Choose best for your use case

### 4️⃣ **Create Custom Training Dataset**

```bash
python3 train_models.py create-dataset src
```

✓ Collects all code from directory  
✓ Generates labels automatically  
✓ Saves as JSON for reproducibility

### 5️⃣ **Benchmark Model Performance**

```bash
python3 train_models.py benchmark
```

✓ Compare speed of different models  
✓ See memory usage  
✓ Identify best for production

---

## 📊 Model Capabilities

| Model           | What It Does                           | Best For                                 | Setup                            |
| --------------- | -------------------------------------- | ---------------------------------------- | -------------------------------- |
| **CodeBERT**    | Deep code embeddings (768-dim vectors) | Understanding code structure, similarity | `pip install transformers torch` |
| **Local Model** | Full LLM inference locally             | Code review, suggestions, generation     | Install Ollama                   |
| **Gemini**      | Cloud AI API (current)                 | Complex analysis, accurate reviews       | Already configured               |
| **Unified**     | Combines all three                     | Comprehensive analysis                   | All of above                     |

---

## 🚀 3-Step Quick Start

### Step 1: Install (One-time)

```bash
cd /home/dev-trivedi/Public/Projects/AI/code_analyst
python3 src/analyzer/custom_models.py install
```

**⏱️ Takes: 5 minutes**

### Step 2: Train on Your Code

```bash
python3 train_models.py train-project . ./models/my-codebert
```

**⏱️ Takes: 10-15 minutes first time (downloads ~350MB)**

### Step 3: Use Your Model

```python
from src.analyzer.custom_models import CodeBertAnalyzer
model = CodeBertAnalyzer("./models/my-codebert")
result = model.analyze_code("def hello(): pass")
```

---

## 🔧 Advanced: Local Models with Ollama

### Download Ollama

- macOS/Linux: `curl https://ollama.ai/install.sh | sh`
- Windows: Download from https://ollama.ai

### Start Server

```bash
ollama serve
# Server runs on http://localhost:11434
```

### Install Code-Specific Model

```bash
ollama pull codellama  # BEST for code (3.3GB)
# or
ollama pull mistral    # Fast (2.6GB)
```

### Use in Your Code

```python
from src.analyzer.custom_models import LocalModelAnalyzer
analyzer = LocalModelAnalyzer(model_name="codellama")
result = analyzer.analyze_code("your python code")
print(result['analysis'])
```

---

## 🐍 Python Examples

### Example 1: Train CodeBERT

```python
from src.analyzer.custom_models import CustomModelTrainer

trainer = CustomModelTrainer()
trainer.train(
    code_samples=[
        "def add(a,b): return a+b",
        "def mul(a,b): return a*b"
    ],
    labels=[1, 1],
    epochs=3
)
trainer.save_trained_model("./models/my-math")
```

### Example 2: Use Trained Model

```python
from src.analyzer.custom_models import CodeBertAnalyzer

model = CodeBertAnalyzer("./models/my-math")
result = model.analyze_code("def divide(a,b): return a/b")
print(f"Complexity: {result['complexity_score']}")
print(f"Insights: {result['insights']}")
```

### Example 3: Compare All Models

```python
from src.analyzer.custom_models import UnifiedCodeAnalyzer

analyzer = UnifiedCodeAnalyzer(
    use_codebert=True,
    use_local=True,
    use_gemini=True
)

code = "def fibonacci(n): return n if n<2 else fibonacci(n-1)+fibonacci(n-2)"
results = analyzer.comparative_analysis(code)

for model_name, analysis in results['unified_analysis']['analyses'].items():
    print(f"\n{model_name}: {analysis}")
```

### Example 4: Train on All Project Files

```python
from src.analyzer.custom_models import CustomModelTrainer
from pathlib import Path

trainer = CustomModelTrainer()
files = list(Path("src").glob("**/*.py"))
samples, labels = trainer.prepare_dataset(files)
print(f"Training on {len(samples)} files...")
trainer.train(samples, labels, epochs=5)
trainer.save_trained_model("./models/project-trained")
```

---

## 🔗 Flask Integration

Add to your Flask app to expose custom models via API:

```python
# In src/app.py
from src.analyzer.model_integration import get_custom_model_integration

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data.get('code')
    model = data.get('model', 'unified')  # NEW

    # Try custom models first
    integration = get_custom_model_integration()

    if model in ['codebert', 'local', 'unified']:
        result = integration.analyze_with_model(code, model)
        if result['status'] == 'success':
            return jsonify(result)

    # Fallback to existing analyzers
    # ...existing code...
```

### API Calls

```bash
# Use CodeBERT
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"def add(a,b): return a+b","model":"codebert"}'

# Use Local Model
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"def add(a,b): return a+b","model":"local"}'

# Use Unified Analysis
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"def add(a,b): return a+b","model":"unified"}'
```

---

## 📚 Full Documentation

### For Detailed Information

- 📖 **Full Guide**: `CUSTOM_MODELS_GUIDE.md`
- ⚡ **Quick Ref**: `CUSTOM_MODELS_QUICK_REF.md`
- 💻 **Code**: `src/analyzer/custom_models.py`
- 🧑‍💼 **Integration**: `src/analyzer/model_integration.py`
- 🛠️ **CLI Tool**: `train_models.py`

### Getting Help

```bash
# Show all available commands
python3 train_models.py help

# Run example
python3 src/analyzer/custom_models.py example

# Show setup instructions
python3 src/analyzer/custom_models.py setup-local
```

---

## ⚙️ System Requirements

### Minimum

- Python 3.8+
- 4GB RAM
- 2GB disk space

### Recommended for Training

- Python 3.9+
- 8GB+ RAM
- GPU (NVIDIA with CUDA) - optional but faster
- 10GB disk space

### For Local Models

- 6-8GB RAM
- ~5GB per model
- CPU or GPU

---

## 🎓 What's Next?

1. ✅ **Try it out**: `python3 train_models.py train-project`
2. ✅ **Compare models**: `python3 train_models.py compare "your code"`
3. ✅ **Setup Ollama**: `ollama serve` and `ollama pull codellama`
4. ✅ **Integrate with Flask**: Add model selection dropdown to UI
5. ✅ **Deploy**: Use trained models in production

---

## 🎁 What You Get

✅ Complete training infrastructure  
✅ Support for 3 different AI approaches  
✅ Easy CLI tools  
✅ Production-ready code  
✅ Full documentation  
✅ Integration ready  
✅ Benchmarking tools  
✅ Example scripts

---

## 🚀 Let's Get Started!

```bash
# 1. Install dependencies
python3 src/analyzer/custom_models.py install

# 2. Train on your project
python3 train_models.py train-project . ./models/my-model

# 3. Use your model
python3 -c "
from src.analyzer.custom_models import CodeBertAnalyzer
model = CodeBertAnalyzer('./models/my-model')
print(model.analyze_code('def test(): pass'))
"
```

---

**Questions? Check `CUSTOM_MODELS_GUIDE.md` for detailed explanations!**

**Ready? Start with: `python3 src/analyzer/custom_models.py install`**

---

**Happy training! 🎓🚀**
