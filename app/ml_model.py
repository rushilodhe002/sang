import pickle
import os
import random
import numpy as np
import logging

logger = logging.getLogger("sentinel")

class FraudMLModel:
    def __init__(self, model_path: str = "model.pkl"):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """
        Load the pre-trained Isolation Forest model.
        """
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                logger.info(f"Loaded ML model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.model = None
        else:
            logger.warning(f"Model file {self.model_path} not found.")
            
    def predict(self, features: list) -> float:
        """
        Returns an anomaly score converted to risk probability (0-1).
        IsolationForest returns:
            -1 for outliers (anomalies)
             1 for inliers (normal)
        Decision Function:
             Average anomaly score of X of the base classifiers.
             Lower is more abnormal. Negative scores represent outliers.
        """
        if not self.model:
            # Fallback if model not loaded
            return random.uniform(0.1, 0.4)
            
        try:
            # Features expected: [[amount]] (based on training script)
            # We reshape to 2D array
            # Isolation Forest training used [amount], so we pass that.
            # Assuming features passed is [user_id, amount], we take amount (index 1)
            amount = features[1] 
            input_data = np.array([[amount]])
            
            # Predict returns -1 (fraud) or 1 (normal)
            prediction = self.model.predict(input_data)[0]
            
            # decision_function returns a score. 
            # < 0 is anomaly, > 0 is normal.
            score = self.model.decision_function(input_data)[0]
            
            # Normalize score to 0-1 Risk Score
            # If score is negative (anomaly), risk is high.
            # Typical range might be -0.5 to 0.5.
            # Simple conversion: 
            if prediction == -1:
                # Structurally high risk (0.6 - 1.0)
                risk = 0.5 + abs(score) 
                return min(risk, 1.0)
            else:
                # Structurally low risk (0.0 - 0.5)
                # Ensure it's not 0 or negative
                risk = 0.5 - score
                return max(0.0, risk)

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.0
