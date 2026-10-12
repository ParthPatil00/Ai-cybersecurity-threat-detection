import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import REPORT_DIR, ALERT_DIR, FIGURE_DIR
from src.detect import run_detection

st.set_page_config(
    page_title="AI Cybersecurity Threat Detection",
    page_icon="🛡️",
    layout="wide",
)
st.title("AI-Powered Cybersecurity Threat Detection")
st.caption("Defensive ML prototype using public or clearly labelled synthetic flow records.")
st.warning("Research prototype. Predictions are indicators for investigation, not confirmation of an incident.")

if st.button("Run Detection Pipeline"):
    with st.spinner("Analyzing records..."):
        run_detection()
    st.success("Detection finished.")

results_path = REPORT_DIR / "detection_results.csv"
alerts_path = ALERT_DIR / "security_alerts.csv"
if not results_path.exists():
    st.info("No results found. Run `python main.py demo` or train models and run `python main.py detect`.")
    st.stop()

results = pd.read_csv(results_path)
alerts = pd.read_csv(alerts_path) if alerts_path.exists() else pd.DataFrame()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records analyzed", f"{len(results):,}")
c2.metric("Attack predictions", f"{(results['predicted_label'] == 'Attack').sum():,}")
c3.metric("Anomaly flags", f"{results['is_anomaly'].astype(bool).sum():,}")
c4.metric("Alerts", f"{len(alerts):,}")

st.subheader("Predicted class distribution")
st.bar_chart(results["predicted_label"].value_counts())

st.subheader("Anomaly scores")
st.line_chart(results["anomaly_score"].reset_index(drop=True))

st.subheader("Detection results")
options = sorted(results["predicted_label"].dropna().unique())
selected = st.multiselect("Filter predicted classes", options, default=options)
filtered = results[results["predicted_label"].isin(selected)]
st.dataframe(filtered.head(1000), use_container_width=True)
st.download_button(
    "Download detection results CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="detection_results.csv",
    mime="text/csv",
)

if not alerts.empty:
    st.subheader("Security alerts")
    st.dataframe(alerts.head(500), use_container_width=True)
    st.download_button(
        "Download security alerts CSV",
        data=alerts.to_csv(index=False).encode("utf-8"),
        file_name="security_alerts.csv",
        mime="text/csv",
    )

for name in ["confusion_matrix.png", "attack_distribution.png", "anomaly_distribution.png"]:
    image_path = FIGURE_DIR / name
    if image_path.exists():
        st.image(str(image_path), caption=name.replace("_", " ").replace(".png", "").title())
