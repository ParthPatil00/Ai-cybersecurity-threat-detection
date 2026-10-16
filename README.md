# 🛡️ AI-Powered Cybersecurity Threat Detection System

A machine learning-based network intrusion detection system that
identifies potentially malicious network traffic using supervised
classification and unsupervised anomaly detection.

## 🚀 Features

- Random Forest model for attack classification
- Isolation Forest for anomaly detection
- Network traffic analysis using the UNSW-NB15 dataset
- Security alert generation and CSV reports
- Interactive Streamlit dashboard
- Attack distribution visualizations
- Modular Python implementation

## 🧠 Machine Learning Models

### Random Forest
Classifies network traffic using features learned from labeled
network traffic data.

### Isolation Forest
Identifies unusual traffic patterns that may require further
investigation.

## 🛠️ Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib
- Streamlit
- UNSW-NB15 dataset

## 📂 Project Structure

```text
AI-Cybersecurity-Threat-Detection/
├── dashboard/
├── data/
│   └── raw/
├── docs/
├── outputs/
│   ├── alerts/
│   ├── figures/
│   └── reports/
├── src/
├── tests/
├── main.py
├── requirements.txt
└── README.md