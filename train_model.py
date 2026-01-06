import numpy as np
from sklearn.ensemble import IsolationForest
import pickle
import os

# 1. Generate Syntax Data (Normal vs Fraud)
# Normal: amount ~ 100-2000
X_normal = np.random.normal(loc=1000, scale=500, size=(500, 1))
# Fraud: amount ~ 5000-10000
X_anomalies = np.random.normal(loc=8000, scale=1000, size=(20, 1))

X = np.concatenate([X_normal, X_anomalies])

# 2. Train Isolation Forest
# contamination=0.05 means we expect ~5% fraud
clf = IsolationForest(random_state=42, contamination=0.05)
clf.fit(X)

# 3. Save Model
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("Model trained and saved to model.pkl")
