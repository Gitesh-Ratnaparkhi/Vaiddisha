# src/services/analytics_service.py
import pandas as pd
import plotly.express as px
from src.repositories.consultation_repository import consultation_repository

def get_patient_history_and_analytics(user_session: dict) -> tuple[pd.DataFrame, object, str]:
    """
    Retrieves consultation history for the logged-in patient and generates
    analytics data and an urgency trend chart.
    """
    email = user_session.get("email", "") if user_session else ""
    if not email:
        empty_df = pd.DataFrame(columns=["ID", "Date", "Symptoms", "Urgency", "Specialty", "Summary"])
        return empty_df, None, "⚠️ Please log in as a patient to view your health history."

    records = consultation_repository.get_consultations_by_patient(email)
    if not records:
        empty_df = pd.DataFrame(columns=["ID", "Date", "Symptoms", "Urgency", "Specialty", "Summary"])
        return empty_df, None, "ℹ️ No consultation history found yet. Complete a triage check to see your records."

    # Convert to DataFrame
    df = pd.DataFrame(records)
    df.rename(columns={
        "id": "ID",
        "created_at": "Date",
        "symptoms": "Symptoms",
        "urgency_level": "Urgency",
        "recommended_specialty": "Specialty",
        "summary": "Summary"
    }, inplace=True)

    # 1. Build Urgency Distribution Chart using Plotly
    urgency_counts = df["Urgency"].value_counts().reset_index()
    urgency_counts.columns = ["Urgency Level", "Count"]

    color_discrete_map = {
        "Low": "#22c55e",
        "Medium": "#eab308",
        "High": "#f97316",
        "Emergency": "#ef4444"
    }

    fig = px.pie(
        urgency_counts,
        names="Urgency Level",
        values="Count",
        title="📊 Triage Risk Level Distribution",
        color="Urgency Level",
        color_discrete_map=color_discrete_map,
        hole=0.4
    )
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))

    summary_msg = f"✅ Loaded **{len(df)}** past consultation record(s)."
    return df, fig, summary_msg