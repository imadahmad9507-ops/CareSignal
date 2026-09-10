from datetime import date

import pandas as pd
import streamlit as st

from database import add_observation, add_patient, get_observations, get_patient, get_patients, init_db
from explanations import generate_explanation
from risk_rules import assess_risk


st.set_page_config(page_title="CareSignal", page_icon="+", layout="wide")
init_db()

DISCLAIMER = (
    "This is an educational prototype using synthetic data. It does not diagnose "
    "medical conditions and does not replace professional medical advice. In an "
    "emergency, contact a doctor or emergency services immediately."
)
RISK_COLORS = {"Stable": "#2f8f62", "Monitor": "#c59627", "Concerning": "#d8773f", "Urgent": "#c94845"}


@st.cache_data(ttl=2)
def patient_list():
    return [dict(patient) for patient in get_patients()]


def assessed_observations(patient_id):
    observations = [dict(item) for item in get_observations(patient_id)]
    assessed = []
    for index, observation in enumerate(observations):
        previous = observations[index - 1] if index else None
        risk, reasons = assess_risk(observation, previous)
        explanation, source = generate_explanation(risk, reasons)
        assessed.append({"observation": observation, "risk": risk, "reasons": reasons, "explanation": explanation, "source": source})
    return assessed


def risk_badge(risk):
    color = RISK_COLORS[risk]
    st.markdown(
        f'<span style="background:{color};color:white;padding:0.35rem 0.7rem;border-radius:999px;font-weight:700">{risk}</span>',
        unsafe_allow_html=True,
    )


def add_patient_form():
    st.subheader("Add a patient")
    with st.form("add_patient"):
        name = st.text_input("Patient name", placeholder="e.g. Ahmed")
        submitted = st.form_submit_button("Create patient")
    if submitted:
        if not name.strip():
            st.error("Enter a patient name.")
        else:
            add_patient(name)
            patient_list.clear()
            st.success("Patient created. Select them from the sidebar.")
            st.rerun()


def check_in_form(patient):
    st.subheader(f"Daily check-in: {patient['name']}")
    with st.form("check_in"):
        first, second, third = st.columns(3)
        observation_date = first.date_input("Date", value=date.today())
        oxygen = second.number_input("Oxygen saturation (%)", 50.0, 100.0, 96.0, 0.1)
        temperature = third.number_input("Temperature (C)", 30.0, 45.0, 37.0, 0.1)
        first, second, third = st.columns(3)
        blood_pressure_sys = first.number_input("Blood pressure: systolic", 50, 250, 120)
        blood_pressure_dia = second.number_input("Blood pressure: diastolic", 30, 150, 80)
        pain_level = third.slider("Pain level", 0, 10, 0)
        first, second, third = st.columns(3)
        breathing = first.selectbox("Breathing difficulty", ["none", "mild", "moderate", "severe"])
        confusion = second.selectbox("Confusion", ["no", "yes"])
        adherence = third.selectbox("Medication taken?", ["yes", "no"])
        notes = st.text_area("Notes", placeholder="Anything else worth remembering?")
        submitted = st.form_submit_button("Save check-in")
    if submitted:
        try:
            add_observation(patient["id"], {"date": observation_date.isoformat(), "oxygen": oxygen, "temperature": temperature, "blood_pressure_sys": blood_pressure_sys, "blood_pressure_dia": blood_pressure_dia, "breathing_difficulty": breathing, "pain_level": pain_level, "confusion": confusion, "medication_adherence": adherence, "notes": notes.strip()})
            st.success("Daily check-in saved.")
            st.rerun()
        except Exception as error:
            st.error(f"Could not save this check-in: {error}")


def patient_detail(patient):
    assessed = assessed_observations(patient["id"])
    st.subheader(patient["name"])
    st.info(DISCLAIMER)
    if not assessed:
        st.warning("No observations yet. Add the first daily check-in below.")
        check_in_form(patient)
        return

    latest = assessed[-1]
    left, right = st.columns([1.4, 1])
    with left:
        st.caption(f"CURRENT SIGNAL / {latest['observation']['date']}")
        risk_badge(latest["risk"])
        st.markdown(f"### {latest['explanation']}")
        st.caption(f"Explanation source: {latest['source']}. Risk level set by deterministic rules.")
    with right:
        st.caption("WHY THIS STATUS")
        for reason in latest["reasons"] or ["No concerning changes detected."]:
            st.write(f"+ {reason}")

    chart_rows = []
    for item in assessed:
        observation = item["observation"]
        chart_rows.append({"Date": observation["date"], "Oxygen (%)": observation["oxygen"], "Temperature (C)": observation["temperature"], "Pain (0-10)": observation["pain_level"]})
    st.subheader("Health trend")
    st.line_chart(pd.DataFrame(chart_rows).set_index("Date"))

    st.subheader("Past observations")
    table_rows = []
    for item in reversed(assessed):
        observation = item["observation"]
        table_rows.append({"Date": observation["date"], "Oxygen": f"{observation['oxygen']}%", "Temperature": f"{observation['temperature']} C", "Breathing": observation["breathing_difficulty"].capitalize(), "Pain": f"{observation['pain_level']}/10", "Signal": item["risk"]})
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
    with st.expander("Record another check-in"):
        check_in_form(patient)


st.markdown("# CareSignal")
st.caption("Explainable health trend monitoring for family caregivers")
with st.sidebar:
    st.header("Caregiver console")
    page = st.radio("Navigate", ["Patient overview", "Add patient"], label_visibility="collapsed")
    st.divider()
    st.caption("Rules decide the risk. Plain language explains it.")

if page == "Add patient":
    add_patient_form()
else:
    patients = patient_list()
    if not patients:
        st.warning("Start by adding a patient.")
        add_patient_form()
    else:
        selected_name = st.sidebar.selectbox("Patient", [patient["name"] for patient in patients])
        selected = next(patient for patient in patients if patient["name"] == selected_name)
        st.sidebar.button("Refresh data", on_click=patient_list.clear)
        patient_detail(selected)
