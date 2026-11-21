
import streamlit as st
import requests

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Loan Prediction System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/predict/"

# ---------------------------------
# CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

.main-title {
    font-size: 34px;
    font-weight: 750;
    color: #17365D;
    margin-bottom: 5px;
}

.subtitle {
    color: #64748B;
    font-size: 16px;
}

.section-title {
    color: #17365D;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 12px;
}

.info-card {
    background-color: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    margin-bottom: 15px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 14px;
    border-color: #E2E8F0;
}

.stButton > button {
    background-color: #17365D;
    color: white;
    border: none;
    border-radius: 9px;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #24558A;
    color: white;
    border: none;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] {
    border-radius: 8px;
}

.footer {
    text-align: center;
    color: #64748B;
    font-size: 13px;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# HEADER
# ---------------------------------

st.markdown("""
<div class="info-card">
    <div style="display:flex; align-items:center; gap:15px;">
        <div style="font-size:45px;">🏦</div>
        <div>
            <div class="main-title">Loan Prediction System</div>
            <div class="subtitle">
                Machine Learning Based Loan Eligibility Prediction
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write(
    "Check your loan eligibility by entering the applicant details below. "
    "Our machine learning model will analyse the information and generate a prediction."
)

st.write("")

# ---------------------------------
# APPLICANT DETAILS
# ---------------------------------

st.markdown(
    '<div class="section-title">👤 Applicant Information</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown("**Personal Details**")

        married = st.selectbox(
            "Marital Status",
            ["Yes", "No"],
            help="Select whether the applicant is married."
        )

        education = st.selectbox(
            "Education",
            ["Graduate", "Not Graduate"]
        )

        income = st.number_input(
            "Applicant Monthly Income",
            min_value=0,
            value=5000,
            step=500,
            help="Enter the applicant income."
        )

    with col2:

        st.markdown("**Loan and Credit Details**")

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0,
            value=150,
            step=10,
            help="Enter the loan amount using the same units as the training dataset."
        )

        credit_history = st.selectbox(
            "Credit History",
            [1, 0],
            format_func=lambda x: "Good (1)" if x == 1 else "Poor (0)",
            help="Select the applicant's credit history."
        )

        st.info(
            "A good credit history is represented by 1, "
            "while a poor credit history is represented by 0."
        )

# ---------------------------------
# PREDICTION BUTTON
# ---------------------------------

st.write("")
st.markdown(
    '<div class="section-title">🔍 Loan Eligibility Check</div>',
    unsafe_allow_html=True
)

predict_col, reset_col = st.columns([3, 1])

with predict_col:
    predict_button = st.button(
        "🚀 Predict Loan Status",
        use_container_width=True
    )

with reset_col:
    reset_button = st.button(
        "↻ Reset",
        use_container_width=True
    )

if reset_button:
    st.rerun()


# ---------------------------------
# PREDICTION PROCESS
# ---------------------------------

if predict_button:

    input_data = {
        "x1": 1 if married == "Yes" else 0,
        "x2": income,
        "x3": loan_amount,
        "x4": 0 if education == "Graduate" else 1,
        "x5": credit_history
    }

    try:
        with st.spinner("Analysing applicant details..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=15
            )

        if response.status_code == 200:

            result = response.json()

            if "prediction" not in result:
                st.error("The API response does not contain a prediction.")
            else:
                prediction = result["prediction"]

                st.write("")
                st.markdown(
                    '<div class="section-title">📊 Prediction Result</div>',
                    unsafe_allow_html=True
                )

                if prediction == 1:

                    st.success(
                        "### ✅ Loan Approved!\n\n"
                        "The machine learning model predicts that "
                        "the applicant is eligible for loan approval."
                    )

                elif prediction == 0:

                    st.error(
                        "### ❌ Loan Not Approved\n\n"
                        "The machine learning model predicts that "
                        "the applicant is not eligible for loan approval."
                    )

                else:
                    st.warning(f"Unexpected prediction result: {prediction}")

                st.caption(
                    "This result is a machine learning prediction, "
                    "not a final decision from a financial institution."
                )

        else:
            st.error(
                f"API Error ({response.status_code}): {response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "⚠️ Unable to connect to the prediction server. "
            "Please make sure the FastAPI backend is running."
        )

    except requests.exceptions.Timeout:
        st.error(
            "The server took too long to respond. Please try again."
        )

    except (ValueError, KeyError):
        st.error(
            "The server returned an invalid response. "
            "Please check your FastAPI output."
        )

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")


# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.markdown("""
<div class="footer">
    <b>Loan Prediction System</b><br>
    Developed using Python | Streamlit | FastAPI | Machine Learning
    <br><br>
    Academic Project | Introduction to Artificial Intelligence
</div>
""", unsafe_allow_html=True)

