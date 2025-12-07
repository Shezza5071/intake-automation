import streamlit as st
from datetime import datetime

# Try importing Snowflake session (works only in Snowflake)
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except Exception:
    session = None

# If not running inside Snowflake, show error
if session is None:
    st.error("❌ This app must run inside Snowflake (Streamlit-in-Snowflake). No active session found.")
    st.stop()

# Ensure table exists before UI loads
session.sql("""
CREATE TABLE IF NOT EXISTS CLIENT_DETAILS (
    First_Name VARCHAR,
    Last_Name VARCHAR,
    Date_of_Birth DATE,
    Email VARCHAR,
    Phone_Main VARCHAR,
    Street_Address VARCHAR,
    Suburb VARCHAR,
    Postcode VARCHAR,
    Gender VARCHAR,
    Contact_First_Name VARCHAR,
    Contact_Last_Name VARCHAR,
    Contact_Phone_Number VARCHAR,
    Contact_Email VARCHAR,
    Client_Type VARCHAR,
    Interpreter_Required VARCHAR,
    Preferred_Language VARCHAR,
    State VARCHAR,
    Region VARCHAR,
    Rostering_Region VARCHAR,
    Tags VARCHAR,
    Created TIMESTAMP_NTZ
)
""").collect()

st.set_page_config(page_title="Referral Form", layout="wide")

# -------------------------------
# Session State Setup
# -------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

st.title("📄 Multi-Step Referral Form")

# -------------------------------
# STEP 1 — Consumer Details
# -------------------------------
if st.session_state.step == 1:
    st.header("Step 1 — Consumer Details")

    st.session_state.first_name = st.text_input("First Name")
    st.session_state.last_name = st.text_input("Last Name")
    st.session_state.dob = st.date_input("Date of Birth")
    st.session_state.phone_main = st.text_input("Phone Number")
    st.session_state.email = st.text_input("Email Address")

    st.subheader("Address")
    st.session_state.street = st.text_input("Street")
    st.session_state.suburb = st.text_input("Suburb")
    st.session_state.postcode = st.text_input("Postcode")
    st.session_state.state = st.text_input("State")

    st.subheader("Gender")
    st.session_state.gender = st.radio(
        "Gender", ["Female", "Male", "Transgender/Non Binary/Gender Diverse", "Prefer not to answer"]
    )

    st.subheader("Preferred Booking Contact")
    st.session_state.preferred_booking = st.multiselect(
        "Select all that apply", ["Phone", "Email", "Contact via Case Manager", "Contact via NOK"]
    )

    st.button("Next", on_click=next_step)

# -------------------------------
# STEP 2 — Next of Kin
# -------------------------------
elif st.session_state.step == 2:
    st.header("Step 2 — Next of Kin")

    st.session_state.nok_first = st.text_input("NOK First Name")
    st.session_state.nok_last = st.text_input("NOK Last Name")
    st.session_state.nok_rel = st.text_input("Relationship")
    st.session_state.nok_phone = st.text_input("Phone Number")
    st.session_state.nok_phone_alt = st.text_input("Alternative Number")
    st.session_state.nok_email = st.text_input("Email")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)

# -------------------------------
# STEP 3 — Referrer / Company
# -------------------------------
elif st.session_state.step == 3:
    st.header("Step 3 — Referrer / Company")

    st.session_state.ref_name = st.text_input("Referrer Name")
    st.session_state.ref_company = st.text_input("Company")
    st.session_state.ref_phone = st.text_input("Phone Number")
    st.session_state.ref_email = st.text_input("Email")
    st.session_state.ref_post1 = st.text_input("Postal Address Line 1")
    st.session_state.ref_post2 = st.text_input("Postal Address Line 2 (optional)")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)

# -------------------------------
# STEP 4 — Payment
# -------------------------------
elif st.session_state.step == 4:
    st.header("Step 4 — Payment & Invoicing")

    st.session_state.payment_type = st.radio(
        "Payment Type",
        ["Home Care Package", "CHSP provider", "Private", "STRC", "Medicare CDM/EPC", "Other"]
    )
    st.session_state.payment_other = st.text_input("If Other, specify")
    st.session_state.provider_name = st.text_input("Provider Name")
    st.session_state.coord_name = st.text_input("Coordinator Name")
    st.session_state.invoice_name = st.text_input("Invoice Contact Name")
    st.session_state.invoice_email = st.text_input("Invoice Email")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)

# -------------------------------
# STEP 5 — Appointment Details
# -------------------------------
elif st.session_state.step == 5:
    st.header("Step 5 — Appointment")

    st.session_state.location = st.radio("Location", ["Face to face", "Telehealth", "No preference"])
    st.session_state.pref_lang = st.text_input("Preferred Language", value="English")
    st.session_state.therapist_gender = st.radio("Therapist Gender", ["Female", "Male", "No preference"])
    st.session_state.interpreter = st.radio("Interpreter required?", ["Yes", "No"])
    st.session_state.unavailability = st.text_area("Regular Unavailability")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)

# -------------------------------
# STEP 6 — Disciplines
# -------------------------------
elif st.session_state.step == 6:
    st.header("Step 6 — Referral Disciplines")

    st.session_state.disciplines = st.multiselect(
        "Disciplines Required",
        ["Occupational Therapy", "Physiotherapy", "Speech Pathology", "Dietetics", "Podiatry"]
    )

    st.session_state.region = st.text_input("Region")
    st.session_state.rostering_region = st.text_input("Rostering Region")
    st.session_state.tags = st.text_input("Tags (comma separated)")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)

# -------------------------------
# STEP 7 — Medical History
# -------------------------------
elif st.session_state.step == 7:
    st.header("Step 7 — Medical History")

    st.session_state.primary_dx = st.text_input("Primary Diagnosis")
    st.session_state.recent_risks = st.text_input("Recent Falls / Risks")
    st.session_state.cog_dx = st.text_input("Cognitive Diagnosis")
    st.session_state.precautions = st.text_input("Specific Precautions")
    st.session_state.other_medical = st.text_input("Other Medical Info")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)

# -------------------------------
# STEP 8 — Submit
# -------------------------------
elif st.session_state.step == 8:
    st.header("Step 8 — Other Info & Submit")

    st.session_state.area_concern = st.text_area("Areas of Concern")
    st.session_state.primary_goal = st.text_area("Primary Goal")
    st.session_state.other_info = st.text_area("Other Relevant Info")
    st.session_state.email_copy = st.checkbox("Send me a copy by email")

    if st.button("Submit"):
        session.sql("""
            INSERT INTO CLIENT_DETAILS (
                First_Name, Last_Name, Date_of_Birth, Email, Phone_Main,
                Street_Address, Suburb, Postcode, Gender,
                Contact_First_Name, Contact_Last_Name, Contact_Phone_Number, Contact_Email,
                Client_Type, Interpreter_Required, Preferred_Language,
                State, Region, Rostering_Region, Tags,
                Created
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP())
        """, (
            st.session_state.first_name,
            st.session_state.last_name,
            st.session_state.dob,
            st.session_state.email,
            st.session_state.phone_main,
            st.session_state.street,
            st.session_state.suburb,
            st.session_state.postcode,
            st.session_state.gender,
            st.session_state.nok_first,
            st.session_state.nok_last,
            st.session_state.nok_phone,
            st.session_state.nok_email,
            st.session_state.payment_type,
            st.session_state.interpreter,
            st.session_state.pref_lang,
            st.session_state.state,
            st.session_state.region,
            st.session_state.rostering_region,
            st.session_state.tags
        )).collect()

        st.success("✅ Referral submitted successfully!")

    st.button("Back", on_click=prev_step)
