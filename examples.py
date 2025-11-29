#!/usr/bin/env python3
"""
Practical Examples: Custom Model Training & Usage
Copy and paste these examples to get started!
"""

# ============================================================
# EXAMPLE 1: Simple CodeBERT Analysis
# ============================================================

def example1_simple_codebert():
    """Analyze code with CodeBERT"""
    from src.analyzer.custom_models import CodeBertAnalyzer
    
    # Initialize model (downloads on first run)
    print("📦 Loading CodeBERT model...")
    model = CodeBertAnalyzer()
    
    # Analyze code
    code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
"""
    
    print("🔍 Analyzing code...")
    result = model.analyze_code(code)
    
    print("\n✅ Analysis Result:")
    print(f"  Model: {result['model']}")
    print(f"  Complexity Score: {result['complexity_score']}/10")
    print(f"  Insights: {result['insights']}")
    
    return result


# ============================================================
# EXAMPLE 2: Train on Sample Code
# ============================================================

def example2_train_simple():
    """Train CodeBERT on sample code"""
    from src.analyzer.custom_models import CustomModelTrainer
    
    print("🚀 Starting Simple Training...")
    
    # Sample code snippets (simple)
    code_samples = [
        # Simple functions
        "def add(a, b): return a + b",
        "def multiply(a, b): return a * b",
        "def subtract(a, b): return a - b",
        
        # Slightly complex
        "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        
        # List operations
        "def filter_positive(numbers):\n    result = []\n    for num in numbers:\n        if num > 0:\n            result.append(num)\n    return result",
    ]
    
    trainer = CustomModelTrainer()
    
    print(f"📊 Prepared {len(code_samples)} samples")
    print("🧠 Training (this takes 5-10 minutes)...")
    
    trainer.train(
        code_samples=code_samples,
        labels=None,  # Auto-generate
        epochs=2,     # Fewer epochs for demo
        batch_size=2  # Smaller batch
    )
    
    print("💾 Saving model...")
    trainer.save_trained_model("./models/demo-model")
    
    print("✅ Training complete! Model saved to ./models/demo-model")
    
    return trainer


# ============================================================
# EXAMPLE 3: Train on Your Project Files
# ============================================================

def example3_train_on_project():
    """Train on your actual project"""
    from src.analyzer.custom_models import CustomModelTrainer
    from pathlib import Path
    
    print("🚀 Training on Project Files...")
    
    # Get Python files
    project_path = "."  # Current directory
    code_files = list(Path(project_path).glob("**/*.py"))
    code_files = [f for f in code_files if "venv" not in str(f) and "__pycache__" not in str(f)]
    
    print(f"📁 Found {len(code_files)} Python files")
    
    if len(code_files) < 2:
        print("⚠️  Need at least 2 files. Not enough files found.")
        return None
    
    # Prepare and train
    trainer = CustomModelTrainer()
    samples, labels = trainer.prepare_dataset(code_files)
    
    print(f"📊 Prepared {len(samples)} samples")
    print("🧠 Training (this takes 10-20 minutes)...")
    
    trainer.train(
        code_samples=samples,
        labels=labels,
        epochs=3,
        batch_size=8
    )
    
    print("💾 Saving model...")
    trainer.save_trained_model("./models/project-codebert")
    
    print("✅ Training complete! Model saved to ./models/project-codebert")
    
    return trainer

# ============================================================
# EXAMPLE 4: Use Trained Model
# ============================================================

def example4_use_trained_model():
    """Use a model you trained"""
    from src.analyzer.custom_models import CodeBertAnalyzer
    
    print("📦 Loading trained model...")
    model = CodeBertAnalyzer("./models/demo-model")
    
    # Test on new code
    test_code = "def process_list(items):\n    processed = []\n    for item in items:\n        if item > 10:\n            processed.append(item * 2)\n    return processed"
    
    print("🔍 Analyzing with trained model...")
    result = model.analyze_code(test_code)
    
    print("\n✅ Result from Trained Model:")
    print(f"  Complexity: {result['complexity_score']}")
    print(f"  Insights: {result['insights']}")
    
    return result


# ============================================================
# EXAMPLE 5: Compare All Models
# ============================================================

def example5_compare_models():
    """Compare CodeBERT, Local, and Gemini"""
    from src.analyzer.custom_models import UnifiedCodeAnalyzer
    import json
    
    print("🔀 Comparing All Models...\n")
    
    analyzer = UnifiedCodeAnalyzer(
        use_codebert=True,
        use_local=False,  # Set True if Ollama running
        use_gemini=True   # Already configured
    )
    
    code = "class Calculator:\n    def add(self, a, b):\n        return a + b\n    \n    def divide(self, a, b):\n        if b == 0:\n            raise ValueError('Cannot divide by zero')\n        return a / b"
    
    print("Analyzing code with all models...\n")
    results = analyzer.comparative_analysis(code)
    
    # Pretty print
    print(json.dumps(
        results,
        indent=2,
        default=str
    ))
    
    return results


# ============================================================
# EXAMPLE 6: Use Local Model (Ollama)
# ============================================================

def example6_local_model():
    """Use local model running via Ollama"""
    from src.analyzer.custom_models import LocalModelAnalyzer
    
    # PREREQUISITE: Start Ollama first
    # ollama serve
    # ollama pull codellama
    
    print("🏠 Using Local Model (Ollama)...")
    
    analyzer = LocalModelAnalyzer(model_name="codellama")
    
    if not analyzer.available:
        print("⚠️  Ollama not running!")
        print("Start with: ollama serve")
        return None
    
    code = "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"
    
    print("🔍 Analyzing with local model...")
    result = analyzer.analyze_code(code)
    
    print("\n✅ Local Model Analysis:")
    print(result['analysis'])
    
    return result


# ============================================================
# EXAMPLE 7: Create Training Dataset from Files
# ============================================================

def example7_create_dataset():
    """Create a training dataset JSON file"""
    from src.analyzer.custom_models import CustomModelTrainer
    from pathlib import Path
    import json
    
    print("📚 Creating Training Dataset...")
    
    # Collect files from directory
    input_dir = "src"  # Your source directory
    code_files = list(Path(input_dir).glob("**/*.py"))
    code_files = [f for f in code_files if "venv" not in str(f)]
    
    print(f"📁 Found {len(code_files)} files")
    
    # Read code
    trainer = CustomModelTrainer()
    samples, labels = trainer.prepare_dataset(code_files)
    
    # Create dataset
    dataset = {
        "code_samples": samples,
        "labels": labels,
        "metadata": {
            "source": input_dir,
            "num_samples": len(samples),
            "average_lines": sum(len(s.split('\n')) for s in samples) // len(samples)
        }
    }
    
    # Save
    output_file = "my_dataset.json"
    with open(output_file, 'w') as f:
        json.dump(dataset, f)
    
    print(f"✅ Dataset saved to {output_file}")
    print(f"  Samples: {len(samples)}")
    print(f"  Size: {len(json.dumps(dataset)) / 1024 / 1024:.2f} MB")
    
    return dataset


# ============================================================
# EXAMPLE 8: Benchmark Models
# ============================================================

def example8_benchmark():
    """Compare speed of different models"""
    from src.analyzer.custom_models import CodeBertAnalyzer, LocalModelAnalyzer
    import time
    
    test_code = "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
    
    print("⚡ Benchmarking Models...\n")
    
    # Benchmark CodeBERT
    try:
        print("⏱️  CodeBERT...")
        model = CodeBertAnalyzer()
        start = time.time()
        result = model.analyze_code(test_code)
        elapsed = time.time() - start
        print(f"   ✓ {elapsed:.2f}s - Complexity: {result['complexity_score']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Benchmark Local Model (if available)
    try:
        print("\n⏱️  Local Model (Ollama)...")
        analyzer = LocalModelAnalyzer()
        if analyzer.available:
            start = time.time()
            result = analyzer.analyze_code(test_code)
            elapsed = time.time() - start
            print(f"   ✓ {elapsed:.2f}s")
        else:
            print("   ⚠️  Ollama not running")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n📊 Benchmarking complete!")


# ============================================================
# EXAMPLE 9: Continuous Training
# ============================================================

def example9_continuous_training():
    """Train model progressively on more data"""
    from src.analyzer.custom_models import CustomModelTrainer
    
    print("📈 Continuous Training Pipeline...\n")
    
    # Initial data
    initial_samples = [
        "def f1(): pass",
        "def f2(): return 42",
        "def f3(a): return a * 2",
    ]
    
    trainer = CustomModelTrainer()
    
    # Training iterations
    for iteration in range(3):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        # Add more samples each iteration
        if iteration > 0:
            initial_samples.extend([
                f"def f_{iteration}_a(): return {iteration}",
                f"def f_{iteration}_b(x): return x + {iteration}",
            ])
        
        print(f"📊 Training on {len(initial_samples)} samples...")
        
        trainer.train(
            code_samples=initial_samples,
            epochs=1,
            batch_size=2
        )
        
        # Save version
        model_path = f"./models/v{iteration + 1}"
        trainer.save_trained_model(model_path)
        print(f"💾 Saved to {model_path}")
    
    print("\n✅ Continuous training complete!")


# ============================================================
# EXAMPLE 10: Full Pipeline
# ============================================================

def example10_full_pipeline():
    """Complete pipeline: create → train → evaluate"""
    from src.analyzer.custom_models import (
        CustomModelTrainer,
        CodeBertAnalyzer,
        UnifiedCodeAnalyzer
    )
    
    print("🚀 FULL PIPELINE: Create → Train → Evaluate\n")
    
    # Step 1: Create dataset
    print("Step 1: Creating Dataset...")
    samples = [
        "def add(a,b): return a+b",
        "def mul(a,b): return a*b",
        "def calc(x): return x*2+1",
        "def process(items): return [x*2 for x in items]",
    ]
    labels = [1, 1, 2, 2]
    print(f"  ✓ {len(samples)} samples")
    
    # Step 2: Train
    print("\nStep 2: Training CodeBERT...")
    trainer = CustomModelTrainer()
    trainer.train(samples, labels, epochs=1, batch_size=2)
    trainer.save_trained_model("./models/full-pipeline")
    print("  ✓ Training complete")
    
    # Step 3: Evaluate
    print("\nStep 3: Evaluating...")
    model = CodeBertAnalyzer("./models/full-pipeline")
    
    test_codes = [
        "def add(a,b): return a+b",
        "def complex_func(data): return sum([x**2 for x in data if x>0])",
    ]
    
    for code in test_codes:
        result = model.analyze_code(code)
        print(f"  Code: {code[:30]}...")
        print(f"    Complexity: {result['complexity_score']}")
    
    print("\n✅ Full pipeline complete!")


# ============================================================
# MAIN: Choose Example to Run
# ============================================================

if __name__ == "__main__":
    import sys
    
    examples = {
        "1": ("Simple CodeBERT", example1_simple_codebert),
        "2": ("Train Simple", example2_train_simple),
        "3": ("Train on Project", example3_train_on_project),
        "4": ("Use Trained Model", example4_use_trained_model),
        "5": ("Compare Models", example5_compare_models),
        "6": ("Local Model (Ollama)", example6_local_model),
        "7": ("Create Dataset", example7_create_dataset),
        "8": ("Benchmark Models", example8_benchmark),
        "9": ("Continuous Training", example9_continuous_training),
        "10": ("Full Pipeline", example10_full_pipeline),
    }
    
    if len(sys.argv) > 1:
        key = sys.argv[1]
        if key in examples:
            name, func = examples[key]
            print(f"\n{'='*60}")
            print(f"📚 Example {key}: {name}")
            print(f"{'='*60}\n")
            try:
                func()
                print(f"\n{'='*60}")
                print("✅ Example completed successfully!")
                print(f"{'='*60}\n")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"❌ Unknown example: {key}")
    else:
        print("\n📚 Available Examples:\n")
        for key, (name, _) in examples.items():
            print(f"  {key}. {name}")
        print(f"\nUsage:")
        print(f"  python3 examples.py 1    # Run example 1")
        print(f"  python3 examples.py 5    # Run example 5")
        print(f"\nOr import and use:")
        print(f"  from examples import example1_simple_codebert")
        print(f"  result = example1_simple_codebert()")
