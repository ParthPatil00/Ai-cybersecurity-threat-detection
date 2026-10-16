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
    page_title="AI Cybersecurity Threat Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp { background: #0b1220; color: #e5edf7; }
    [data-testid="stSidebar"] { background: #101a2b; border-right: 1px solid #24334a; }
    [data-testid="stSidebar"] * { color: #dce7f5; }
    .block-container { padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1500px; }
    .hero {
        padding: 1.35rem 1.5rem; border-radius: 18px;
        background: linear-gradient(120deg, #14243b 0%, #162e43 55%, #173b45 100%);
        border: 1px solid #29465a; margin-bottom: 1rem;
    }
    .hero-kicker { color: #62d6c6; text-transform: uppercase; letter-spacing: .16em;
        font-size: .72rem; font-weight: 800; margin-bottom: .45rem; }
    .hero h1 { color: #f2f7ff; font-size: 2rem; margin: 0 0 .4rem 0; }
    .hero p { color: #b9c9dc; margin: 0; font-size: .98rem; }
    .section-title { color: #eaf2fc; font-size: 1.15rem; font-weight: 700; margin: .6rem 0 .7rem; }
    div[data-testid="stMetric"] { background: #111e30; padding: 1rem 1.1rem;
        border: 1px solid #25364d; border-radius: 14px; }
    div[data-testid="stMetricLabel"] { color: #9fb3ca; }
    div[data-testid="stMetricValue"] { color: #f3f7ff; }
    div[data-testid="stDataFrame"] { border: 1px solid #25364d; border-radius: 12px; overflow: hidden; }
    .note { background: #2a2417; border: 1px solid #65522b; color: #f1dba8;
        padding: .75rem 1rem; border-radius: 10px; font-size: .88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🛡️AI CYBERSECURITY ")
    st.caption("Threat Detection & Monitoring")
    st.divider()
    page = st.radio(
        "WORKSPACE",
        ["Overview", "Detection records", "Security alerts", "Visual reports"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("### Pipeline")
    if st.button("▶ Run detection", use_container_width=True, type="primary"):
        try:
            with st.spinner("Analyzing network records..."):
                run_detection()
            st.success("Detection pipeline completed.")
            st.rerun()
        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")
    if st.button("↻ Refresh data", use_container_width=True):
        st.rerun()
    st.caption("Data source: local detection CSV reports")

st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">Security analytics · ML prototype</div>
      <h1>AI-Powered Cybersecurity Threat Detection System</h1>
      <p>Review model predictions, investigate suspicious records, and export reports from one workspace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="note">Research prototype: alerts indicate records that need investigation; they are not confirmed security incidents. This dashboard reads saved dataset/replay results and does not capture live network packets.</div>',
    unsafe_allow_html=True,
)

results_path = REPORT_DIR / "detection_results.csv"
alerts_path = ALERT_DIR / "security_alerts.csv"

if not results_path.exists():
    st.info("No detection report is available yet. Choose **Run detection** in the sidebar, or run `python main.py demo` from the project root.")
    st.stop()

try:
    results = pd.read_csv(results_path)
except Exception as exc:
    st.error(f"Could not read detection results: {exc}")
    st.stop()

alerts = pd.DataFrame()
if alerts_path.exists():
    try:
        alerts = pd.read_csv(alerts_path)
    except Exception:
        alerts = pd.DataFrame()

# Normalize columns for safe, readable filtering
if "predicted_label" not in results.columns:
    results["predicted_label"] = "Unknown"
if "is_anomaly" not in results.columns:
    results["is_anomaly"] = False
if "anomaly_score" not in results.columns:
    results["anomaly_score"] = 0.0
results["is_anomaly"] = results["is_anomaly"].astype(str).str.lower().isin(["true", "1", "yes"])

attack_count = int((results["predicted_label"] == "Attack").sum())
anomaly_count = int(results["is_anomaly"].sum())
alert_count = len(alerts)
benign_count = int((results["predicted_label"] == "Benign").sum())
attack_rate = (attack_count / len(results) * 100) if len(results) else 0

# ---------- Pages ----------
if page == "Overview":
    st.markdown('<div class="section-title">Environment overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Records analyzed", f"{len(results):,}")
    c2.metric("Attack predictions", f"{attack_count:,}", f"{attack_rate:.1f}% of records")
    c3.metric("Anomaly flags", f"{anomaly_count:,}")
    c4.metric("Generated alerts", f"{alert_count:,}")

    left, right = st.columns([1.15, 1])
    with left:
        st.markdown('<div class="section-title">Predicted traffic classes</div>', unsafe_allow_html=True)
        distribution = results["predicted_label"].fillna("Unknown").value_counts().rename_axis("Class").reset_index(name="Records")
        st.bar_chart(distribution.set_index("Class"), use_container_width=True)
    with right:
        st.markdown('<div class="section-title">Alert severity</div>', unsafe_allow_html=True)
        if not alerts.empty and "severity" in alerts.columns:
            severity = alerts["severity"].fillna("Unknown").value_counts().rename_axis("Severity").reset_index(name="Alerts")
            st.bar_chart(severity.set_index("Severity"), use_container_width=True)
        else:
            st.info("No alert severity data is available.")

    st.markdown('<div class="section-title">Recent alerts requiring review</div>', unsafe_allow_html=True)
    if not alerts.empty:
        st.dataframe(alerts.head(8), use_container_width=True, hide_index=True)
    else:
        st.success("No alerts are currently listed in the saved report.")

    st.download_button(
        "Download full detection report",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="detection_results.csv",
        mime="text/csv",
    )

elif page == "Detection records":
    st.markdown('<div class="section-title">Search and filter detection records</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1.2])
    classes = sorted(results["predicted_label"].dropna().astype(str).unique().tolist())
    with col1:
        selected_classes = st.multiselect("Predicted class", classes, default=classes)
    with col2:
        anomaly_filter = st.selectbox("Anomaly status", ["All records", "Anomaly flagged", "Not flagged"])
    with col3:
        search = st.text_input("Search visible text", placeholder="e.g. Attack, Generic, EVENT...")

    filtered = results[results["predicted_label"].astype(str).isin(selected_classes)]
    if anomaly_filter == "Anomaly flagged":
        filtered = filtered[filtered["is_anomaly"]]
    elif anomaly_filter == "Not flagged":
        filtered = filtered[~filtered["is_anomaly"]]
    if search.strip():
        mask = filtered.astype(str).apply(lambda col: col.str.contains(search.strip(), case=False, na=False)).any(axis=1)
        filtered = filtered[mask]

    st.caption(f"Showing {len(filtered):,} of {len(results):,} records")
    st.dataframe(filtered, use_container_width=True, hide_index=True, height=480)
    st.download_button(
        "Download filtered records CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_detection_records.csv",
        mime="text/csv",
    )

elif page == "Security alerts":
    st.markdown('<div class="section-title">Alert investigation queue</div>', unsafe_allow_html=True)
    if alerts.empty:
        st.success("No saved security alerts found.")
    else:
        alert_view = alerts.copy()
        a1, a2, a3 = st.columns(3)
        severities = sorted(alert_view["severity"].dropna().astype(str).unique()) if "severity" in alert_view else []
        with a1:
            chosen_severity = st.multiselect("Severity", severities, default=severities)
        with a2:
            if "predicted_label" in alert_view:
                labels = sorted(alert_view["predicted_label"].dropna().astype(str).unique())
                chosen_labels = st.multiselect("Predicted label", labels, default=labels)
            else:
                chosen_labels = []
        with a3:
            query = st.text_input("Search alerts", placeholder="Event ID or reason")

        if "severity" in alert_view:
            alert_view = alert_view[alert_view["severity"].astype(str).isin(chosen_severity)]
        if "predicted_label" in alert_view:
            alert_view = alert_view[alert_view["predicted_label"].astype(str).isin(chosen_labels)]
        if query.strip():
            mask = alert_view.astype(str).apply(lambda col: col.str.contains(query.strip(), case=False, na=False)).any(axis=1)
            alert_view = alert_view[mask]

        st.caption(f"{len(alert_view):,} alerts match the current filters")
        st.dataframe(alert_view, use_container_width=True, hide_index=True, height=480)
        st.download_button(
            "Download filtered alerts CSV",
            data=alert_view.to_csv(index=False).encode("utf-8"),
            file_name="filtered_security_alerts.csv",
            mime="text/csv",
        )

else:
    st.markdown('<div class="section-title">Model and traffic visual reports</div>', unsafe_allow_html=True)
    shown = False
    for name in ["confusion_matrix.png", "attack_distribution.png", "anomaly_distribution.png"]:
        image_path = FIGURE_DIR / name
        if image_path.exists():
            shown = True
            st.markdown(f"**{name.replace('_', ' ').replace('.png', '').title()}**")
            st.image(str(image_path), use_container_width=True)
    if not shown:
        st.info("No saved figures found yet. Run model evaluation or detection to generate available plots.")

st.divider()
st.caption("AI CYBERSECURITY · AI-powered cybersecurity threat detection · Defensive research prototype")
