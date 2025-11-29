#!/usr/bin/env python3
"""
Practical training scripts for CodeBERT and custom models
Run this to easily train on your code
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# 1. TRAIN ON YOUR PROJECT
# ============================================================

def train_on_project(project_path: str = ".", output_model: str = "./models/custom-codebert"):
    """Train CodeBERT on your entire project"""
    
    print("\n" + "="*60)
    print("🚀 Training CodeBERT on Your Project")
    print("="*60 + "\n")
    
    # Import here to avoid early errors
    from src.analyzer.custom_models import CustomModelTrainer
    
    # 1. Collect code files
    print("📁 Collecting Python files...")
    code_files = list(Path(project_path).glob("**/*.py"))
    code_files = [f for f in code_files if "venv" not in str(f) and "__pycache__" not in str(f)]
    print(f"   Found {len(code_files)} files\n")
    
    if len(code_files) < 2:
        print("⚠️  Need at least 2 Python files to train. Not enough files found.")
        return
    
    # 2. Prepare dataset
    print("📊 Preparing dataset...")
    trainer = CustomModelTrainer()
    code_samples, labels = trainer.prepare_dataset(code_files)
    print(f"   Prepared {len(code_samples)} samples")
    print(f"   Avg file size: {sum(len(s.split()) for s in code_samples) // len(code_samples)} words\n")
    
    # 3. Train
    print("🧠 Training CodeBERT...")
    print("   (This may take 5-15 minutes on first run)")
    trainer.train(
        code_samples=code_samples,
        labels=labels,
        epochs=3,
        batch_size=8
    )
    
    # 4. Save
    print(f"\n💾 Saving model to {output_model}...")
    trainer.save_trained_model(output_model)
    
    print("\n✅ Training complete!")
    print(f"\nTo use your trained model:")
    print(f"  from src.analyzer.custom_models import CodeBertAnalyzer")
    print(f"  model = CodeBertAnalyzer('{output_model}')")
    print(f"  result = model.analyze_code('your code here')")


# ============================================================
# 2. TRAIN ON SPECIFIC DATASET
# ============================================================

def train_on_dataset(data_file: str, output_model: str = "./models/custom-codebert"):
    """Train on specific code dataset (JSON format)"""
    
    print("\n" + "="*60)
    print("📚 Training on Dataset")
    print("="*60 + "\n")
    
    # Load dataset
    print(f"📖 Loading dataset from {data_file}...")
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    code_samples = data.get('code_samples', data.get('samples', []))
    labels = data.get('labels', None)
    
    print(f"   Loaded {len(code_samples)} samples\n")
    
    # Train
    from src.analyzer.custom_models import CustomModelTrainer
    trainer = CustomModelTrainer()
    
    print("🧠 Training CodeBERT...")
    trainer.train(
        code_samples=code_samples,
        labels=labels,
        epochs=5,
        batch_size=8
    )
    
    print(f"\n💾 Saving model to {output_model}...")
    trainer.save_trained_model(output_model)
    
    print("\n✅ Training complete!")


# ============================================================
# 3. COMPARE MODELS
# ============================================================

def compare_models(code: str):
    """Compare all available models on same code"""
    
    print("\n" + "="*60)
    print("🔀 Comparing All Models")
    print("="*60 + "\n")
    
    print(f"📝 Analyzing code:\n{code[:200]}...\n")
    
    from src.analyzer.custom_models import UnifiedCodeAnalyzer
    
    analyzer = UnifiedCodeAnalyzer(
        use_codebert=True,
        use_local=False,
        use_gemini=True
    )
    
    print("Running analysis with all models...\n")
    results = analyzer.comparative_analysis(code)
    
    print("📊 Results:\n")
    print(json.dumps(results, indent=2, default=str))
    
    # Summary
    print("\n📈 Model Comparison Summary:")
    print(f"   Models used: {results['unified_analysis']['total_models']}")
    for model in results['unified_analysis']['models_used']:
        print(f"   ✓ {model}")


# ============================================================
# 4. CREATE TRAINING DATASET
# ============================================================

def create_dataset_from_files(input_dir: str, output_file: str = "dataset.json"):
    """Create training dataset from code files"""
    
    print("\n" + "="*60)
    print("📚 Creating Training Dataset")
    print("="*60 + "\n")
    
    print(f"📁 Reading code from {input_dir}...\n")
    
    code_files = list(Path(input_dir).glob("**/*.py"))
    code_files = [f for f in code_files if "venv" not in str(f) and "__pycache__" not in str(f)]
    
    code_samples = []
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                if len(code.strip()) > 0:
                    code_samples.append(code)
        except:
            pass
    
    print(f"✅ Found {len(code_samples)} valid Python files\n")
    
    # Auto-generate labels
    labels = [len(code.split('\n')) % 10 for code in code_samples]
    
    # Create dataset
    dataset = {
        "code_samples": code_samples,
        "labels": labels,
        "metadata": {
            "source": input_dir,
            "count": len(code_samples),
            "file_types": ["python"]
        }
    }
    
    # Save
    print(f"💾 Saving dataset to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"✅ Dataset created!")
    print(f"\nDataset info:")
    print(f"   Samples: {len(code_samples)}")
    print(f"   File: {output_file}")
    print(f"\nTo train on this dataset:")
    print(f"   python3 train_models.py train-dataset {output_file}")


# ============================================================
# 5. BENCHMARK MODELS
# ============================================================

def benchmark_models(test_code: str = None):
    """Benchmark different models"""
    
    if test_code is None:
        test_code = """
def process_data(items):
    results = []
    for item in items:
        if item > 0:
            results.append(item * 2)
    return results
"""
    
    print("\n" + "="*60)
    print("⚡ Benchmarking Models")
    print("="*60 + "\n")
    
    import time
    from src.analyzer.custom_models import CodeBertAnalyzer, LocalModelAnalyzer
    
    results = {}
    
    # Benchmark CodeBERT
    try:
        print("⏱️  Benchmarking CodeBERT...")
        codebert = CodeBertAnalyzer()
        start = time.time()
        result = codebert.analyze_code(test_code)
        elapsed = time.time() - start
        results['CodeBERT'] = {
            'time': f"{elapsed:.2f}s",
            'complexity': result.get('complexity_score')
        }
        print(f"   ✓ {elapsed:.2f}s - Complexity: {result.get('complexity_score')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Benchmark Local Model
    try:
        print("\n⏱️  Benchmarking Local Model...")
        local = LocalModelAnalyzer()
        if local.available:
            start = time.time()
            result = local.analyze_code(test_code)
            elapsed = time.time() - start
            results['Local'] = {'time': f"{elapsed:.2f}s"}
            print(f"   ✓ {elapsed:.2f}s")
        else:
            print("   ⚠️  Local model not running")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n📊 Benchmark Results:")
    for model, metrics in results.items():
        print(f"   {model}: {metrics}")


# ============================================================
# 6. MAIN CLI
# ============================================================

def print_help():
    """Print help message"""
    help_text = """
🤖 Custom Model Training CLI

Usage:
  python3 train_models.py COMMAND [OPTIONS]

Commands:

  train-project [PATH] [OUTPUT]
    Train CodeBERT on your project
    Args:
      PATH    - Project directory (default: .)
      OUTPUT  - Output model path (default: ./models/custom-codebert)
    
    Example:
      python3 train_models.py train-project . ./models/my-model
      python3 train_models.py train-project src

  train-dataset FILE [OUTPUT]
    Train on specific dataset (JSON format)
    Args:
      FILE    - Dataset JSON file
      OUTPUT  - Output model path (default: ./models/custom-codebert)
    
    Example:
      python3 train_models.py train-dataset dataset.json

  create-dataset INPUT [OUTPUT]
    Create training dataset from code files
    Args:
      INPUT   - Directory with Python files
      OUTPUT  - Output JSON file (default: dataset.json)
    
    Example:
      python3 train_models.py create-dataset src

  compare CODE
    Compare all available models on code
    
    Example:
      python3 train_models.py compare "def hello(): pass"

  benchmark
    Benchmark model performance
    
    Example:
      python3 train_models.py benchmark

  help
    Show this message

Examples:

  # Create dataset from your project
  python3 train_models.py create-dataset src code_dataset.json

  # Train CodeBERT on dataset
  python3 train_models.py train-dataset code_dataset.json

  # Train on entire project
  python3 train_models.py train-project .

  # Compare models
  python3 train_models.py compare "def add(a,b): return a+b"

  # Benchmark
  python3 train_models.py benchmark
"""
    print(help_text)


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command == "train-project":
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        output = sys.argv[3] if len(sys.argv) > 3 else "./models/custom-codebert"
        train_on_project(path, output)
    
    elif command == "train-dataset":
        if len(sys.argv) < 3:
            print("❌ Please provide dataset file")
            print("Usage: python3 train_models.py train-dataset FILE [OUTPUT]")
            return
        data_file = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else "./models/custom-codebert"
        train_on_dataset(data_file, output)
    
    elif command == "create-dataset":
        if len(sys.argv) < 3:
            print("❌ Please provide input directory")
            print("Usage: python3 train_models.py create-dataset INPUT [OUTPUT]")
            return
        input_dir = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else "dataset.json"
        create_dataset_from_files(input_dir, output)
    
    elif command == "compare":
        if len(sys.argv) < 3:
            code = 'def hello(): pass'
        else:
            code = sys.argv[2]
        compare_models(code)
    
    elif command == "benchmark":
        benchmark_models()
    
    elif command in ["help", "-h", "--help"]:
        print_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
