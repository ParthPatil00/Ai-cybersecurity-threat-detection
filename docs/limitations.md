# Limitations and Responsible Interpretation

- Public datasets may not represent modern enterprise environments.
- A predicted attack is not a confirmed incident.
- An anomaly is not necessarily malicious.
- False positives and false negatives are expected.
- Synthetic demo data is artificial and must not be presented as real-world evaluation.
- The current system processes CSV records, not live network packets.
- Phishing email and executable malware analysis are not implemented.
- Model performance depends on schema, sampling, class balance, and dataset provenance.
- Serialized Joblib models should only be loaded from trusted sources.
