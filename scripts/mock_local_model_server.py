#!/usr/bin/env python3
"""Small mock server that mimics a local model API (Ollama-like)

Provides:
- GET /api/tags  -> returns a models list
- POST /api/generate -> returns a mock generated response

Use this to test local-model detection and the UI without installing Ollama.
"""
from flask import Flask, jsonify, request
import argparse

app = Flask(__name__)

MOCK_MODELS = [
    {"id": "codellama", "name": "codellama"},
    {"id": "mistral", "name": "mistral"}
]

@app.route('/api/tags', methods=['GET'])
def tags():
    return jsonify({"models": MOCK_MODELS})

@app.route('/v1/models', methods=['GET'])
def v1_models():
    return jsonify({"models": [ {"id": m['id']} for m in MOCK_MODELS ]})

@app.route('/models', methods=['GET'])
def models():
    return jsonify(MOCK_MODELS)

@app.route('/api/generate', methods=['POST'])
def generate():
    payload = request.get_json() or {}
    model = payload.get('model') or payload.get('model_name') or 'codellama'
    prompt = payload.get('prompt', '')

    # A trivial mock reply
    reply = f"Mock reply from {model}: Summary length {len(prompt)} characters."
    return jsonify({"response": reply})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=11434)
    args = parser.parse_args()
    print(f"Starting mock local-model server on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port)
