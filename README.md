
# DrDoS DNS Detection — Project Overview

## Introduction (Description & Overview)

This project implements an end-to-end machine learning pipeline to detect DNS-based Distributed Reflection of Service (DrDoS) attacks using labeled network flow data. It contains data preprocessing, model training, evaluation, model persistence, and a lightweight Flask-based inference service for demonstration. The repository provides `train.py` for experiments and `app.py` to serve predictions.

## Problem Statement

DNS amplification and reflection attacks (DrDoS) use open DNS resolvers to flood targets with amplified responses. These attacks can cause service outages and are difficult to separate from legitimate DNS traffic due to volume, traffic variability, and class imbalance in training data. The objective is to build a classifier that reliably identifies DrDoS flows with high recall while keeping false positives manageable for operational use.

## Solution

The solution is a supervised learning approach that transforms the raw `dataset/DrDoS_DNS.csv` into feature vectors, trains classification models, evaluates them with robust metrics, and exports the best-performing model for inference:

- Data ingestion and cleaning: normalization, missing-value handling, and optional categorical encoding.
- Feature engineering: statistics such as packet counts, byte counts, and time-related features derived from flows.
- Model training: experiments with models such as Random Forest or gradient-boosted trees, hyperparameter tuning, and cross-validation.
- Evaluation: precision, recall, F1, ROC-AUC and confusion matrices to select a model that balances detection and false-positive rates.
- Serving: a small Flask app (`app.py`) exposes an API and demo UI to make predictions using the saved model artifact.

## System Pipeline Architecture

The following architecture describes the end-to-end flow from raw dataset ingestion to live inference in the Flask web interface.

```mermaid
flowchart LR
    A[Raw CSV Dataset] --> B[Data Ingestion & Cleaning]
    B --> C[Feature Engineering]
    C --> D[Model Training & Validation]
    D --> E[Model Persistence (`model.pkl`, `scaler.pkl`, `features.pkl`)]
    E --> F[Flask Inference Service]
    F --> G[User Interface / Prediction Output]
```

1. **Raw CSV Dataset**: Start with network flow data from `dataset/DrDoS_DNS.csv`.
2. **Data Ingestion & Cleaning**: Load data, handle missing values, normalize features, and prepare data for modeling.
3. **Feature Engineering**: Compute relevant flow statistics and select the final feature set used by the classifier.
4. **Model Training & Validation**: Train, tune, and evaluate machine learning models using the prepared dataset.
5. **Model Persistence**: Save the trained model, scaler, and feature list as serialized artifacts for reuse.
6. **Flask Inference Service**: Load saved artifacts in `app.py`, accept user inputs, scale features, and make predictions.
7. **User Interface / Prediction Output**: Display attack detection results in the browser.

## Features

- Preprocessing pipeline for CSV network flow data.
- Configurable training script with model selection and hyperparameter search.
- Class imbalance handling (sample weighting or resampling strategies).
- Model evaluation and reporting (confusion matrix, precision/recall/F1, ROC-AUC).
- Model persistence using joblib/pickle for reproducible inference.
- Lightweight REST API and demo UI via Flask for single-sample or batch predictions.

## Scope

Included:

- Offline dataset-driven training and evaluation using `dataset/DrDoS_DNS.csv`.
- Local model serving and manual demo UI for validation and testing.

Excluded (out of scope):

- Production deployment, auto-scaling, and secure production hardening.
- Real-time packet capture/streaming ingestion (e.g., Kafka, PCAP sensors).
- Active mitigation (automatic blocking or firewall rule enforcement).
- Continuous retraining pipelines and drift detection (future enhancement).

## Technology Descriptions

- **Python**: Primary language for data processing, model training, and serving.
- **Pandas / NumPy**: Data manipulation and numeric operations.
- **scikit-learn**: Preprocessing tools, model implementations (RandomForest, LogisticRegression), evaluation and pipelines.
- **imbalanced-learn (optional)**: Resampling techniques like SMOTE to address class imbalance.
- **joblib / pickle**: Model serialization and persistence.
- **Flask**: Lightweight web framework to serve inference endpoints and demo UI (`app.py`).
- **Virtual Environment**: `ve/` contains the project's isolated Python environment; activate before running scripts.

## Next Steps (optional)

- Add a `requirements.txt` exported from the `ve/` environment for reproducibility.
- Add examples of API requests and a short `usage` section in this README.
- Add unit tests for preprocessing and inference functions.

---

If you want, I can also add a concise executive summary for stakeholders and create a `requirements.txt` based on the environment in `ve/Lib/site-packages`.
