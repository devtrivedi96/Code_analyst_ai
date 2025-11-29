#!/usr/bin/env python3
"""
Integration layer for custom models with Flask app
"""

import logging
from src.analyzer.custom_models import (
    CodeBertAnalyzer,
    LocalModelAnalyzer,
    UnifiedCodeAnalyzer
)

logger = logging.getLogger(__name__)


class CustomModelIntegration:
    """Integrate custom models into Flask analyzer"""
    
    def __init__(self):
        """Initialize custom model integration"""
        self.codebert = None
        self.local_model = None
        self.unified_analyzer = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize available models"""
        # Try CodeBERT
        try:
            self.codebert = CodeBertAnalyzer()
            logger.info("✅ CodeBERT loaded")
        except Exception as e:
            logger.warning(f"CodeBERT unavailable: {e}")
        
        # Try local models
        try:
            self.local_model = LocalModelAnalyzer()
            if self.local_model.available:
                logger.info(f"✅ Local model ({self.local_model.model_name}) available")
        except Exception as e:
            logger.warning(f"Local models unavailable: {e}")
        
        # Initialize unified analyzer
        try:
            self.unified_analyzer = UnifiedCodeAnalyzer(
                use_codebert=bool(self.codebert),
                use_local=self.local_model.available if self.local_model else False,
                use_gemini=True
            )
            logger.info("✅ Unified analyzer initialized")
        except Exception as e:
            logger.warning(f"Unified analyzer error: {e}")
    
    def get_available_models(self) -> list:
        """Get list of available custom models"""
        models = []
        
        if self.codebert:
            models.append({
                "id": "codebert",
                "name": "CodeBERT (microsoft/codebert-base)",
                "type": "transformer",
                "description": "Deep code understanding with embeddings"
            })
        
        if self.local_model and self.local_model.available:
            models.append({
                "id": "local",
                "name": f"Local Model ({self.local_model.model_name})",
                "type": "local",
                "description": "Local running model (Ollama)"
            })
        
        models.append({
            "id": "unified",
            "name": "Unified Analysis",
            "type": "hybrid",
            "description": "Combines all available models"
        })
        
        return models
    
    def analyze_with_model(self, code: str, model_id: str) -> dict:
        """Analyze code with specific custom model"""
        
        if model_id == "codebert" and self.codebert:
            return {
                "model": "CodeBERT",
                "result": self.codebert.analyze_code(code),
                "status": "success"
            }
        
        elif model_id == "local" and self.local_model and self.local_model.available:
            return {
                "model": "Local Model",
                "result": self.local_model.analyze_code(code),
                "status": "success"
            }
        
        elif model_id == "unified" and self.unified_analyzer:
            return {
                "model": "Unified Analysis",
                "result": self.unified_analyzer.comparative_analysis(code),
                "status": "success"
            }
        
        else:
            return {
                "model": model_id,
                "result": None,
                "status": "error",
                "message": f"Model {model_id} not available"
            }
    
    def train_codebert_on_code(self, code_samples: list, labels: list = None, 
                              epochs: int = 3, batch_size: int = 8) -> dict:
        """Fine-tune CodeBERT on custom code"""
        if not self.codebert:
            return {
                "status": "error",
                "message": "CodeBERT not initialized"
            }
        
        try:
            success = self.codebert.train_on_custom_data(
                code_samples, labels, epochs, batch_size
            )
            return {
                "status": "success" if success else "error",
                "samples": len(code_samples),
                "epochs": epochs,
                "message": "Training completed" if success else "Training failed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def save_custom_model(self, path: str) -> dict:
        """Save trained model"""
        if not self.codebert:
            return {
                "status": "error",
                "message": "CodeBERT not initialized"
            }
        
        try:
            self.codebert.save_model(path)
            return {
                "status": "success",
                "path": path,
                "message": f"Model saved to {path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


# Singleton instance
_integration = None


def get_custom_model_integration() -> CustomModelIntegration:
    """Get singleton instance"""
    global _integration
    if _integration is None:
        _integration = CustomModelIntegration()
    return _integration
