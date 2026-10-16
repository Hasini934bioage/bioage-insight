import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.set_page_config(
    page_title="BioAge Insight",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
:root {
    --ink: #17324d;
    --muted: #61758a;
    --teal: #087f8c;
    --mint: #18a999;
    --line: #dbe7ee;
    --surface: #ffffff;
    --canvas: #f4f8fb;
}

.stApp {
    background: linear-gradient(145deg, #f4f8fc 0%, #edf7f5 100%);
    color: var(--ink);
}
.block-container {
    max-width: 1480px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4 {
    color: var(--ink);
    letter-spacing: -0.02em;
}
h1 { font-size: clamp(2rem, 3vw, 3rem); }
h2 { margin-top: .4rem; }
p, li, label, [data-testid="stMarkdownContainer"] {
    color: var(--ink);
}
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    box-shadow: 0 5px 18px rgba(23, 50, 77, .055);
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: var(--teal) !important;
    font-weight: 750 !important;
}
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(100deg, var(--teal), var(--mint));
    color: white;
    border: 0;
    border-radius: 10px;
    min-height: 2.7rem;
    font-weight: 650;
    box-shadow: 0 4px 10px rgba(8, 127, 140, .14);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 7px 16px rgba(8, 127, 140, .2);
}
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    background: white !important;
    color: var(--ink) !important;
    border: 1px solid #cbdce5 !important;
    border-radius: 9px !important;
}
[data-testid="stWidgetLabel"] label {
    color: var(--ink) !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"] {
    font-weight: 650;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,.78);
    border: 1px solid var(--line);
    border-radius: 13px;
    overflow: hidden;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,.88);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: .45rem;
    box-shadow: 0 4px 15px rgba(23,50,77,.035);
}
[data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
    gap: 1rem;
}
.stRadio > div, .stSelectbox, .stNumberInput {
    min-width: 0;
}
hr {
    border-color: var(--line);
}
.hero-banner {
    position: relative;
    overflow: hidden;
    padding: clamp(1.6rem, 3.5vw, 3rem);
    margin: .2rem 0 1.2rem;
    border-radius: 22px;
    background: linear-gradient(120deg, #123b50 0%, #087f8c 65%, #18a999 100%);
    color: white;
    box-shadow: 0 12px 28px rgba(18, 59, 80, .16);
}
.hero-banner h1, .hero-banner p, .hero-banner .hero-tag {
    color: white !important;
}
.hero-tag {
    display: inline-block;
    font-size: .72rem;
    font-weight: 750;
    letter-spacing: .14em;
    opacity: .88;
    margin-bottom: .5rem;
}
.hero-banner h1 {
    margin: 0;
    line-height: 1.12;
}
.hero-subtitle {
    font-size: clamp(1.05rem, 1.8vw, 1.35rem);
    font-weight: 650;
    margin: .5rem 0 .35rem;
}
.hero-description {
    max-width: 760px;
    margin-bottom: 0;
    opacity: .92;
}
.hero-banner:after {
    content: "🧬";
    position: absolute;
    right: 4%;
    top: 12%;
    font-size: clamp(4rem, 9vw, 8rem);
    opacity: .14;
    transform: rotate(-12deg);
    pointer-events: none;
}
.section-intro {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    background: linear-gradient(100deg, #e2f7f3, #edf3ff);
    border: 1px solid #cde8e7;
    margin: .4rem 0 1rem;
}
.person-card-a {
    border-top: 5px solid #087f8c;
    background: linear-gradient(180deg, #e8f8f7 0%, #ffffff 40%);
    border-radius: 16px;
    padding: 1rem;
}
.person-card-b {
    border-top: 5px solid #7565d8;
    background: linear-gradient(180deg, #f0edff 0%, #ffffff 40%);
    border-radius: 16px;
    padding: 1rem;
}
.result-strip {
    border-radius: 16px;
    padding: 1rem;
    background: linear-gradient(110deg, #123b50, #087f8c);
    color: white;
    margin: .6rem 0 1rem;
}
.result-strip h3, .result-strip p {
    color: white !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(225,238,245,.7);
    border-radius: 13px;
    padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: white;
}
[data-testid="stAlert"] {
    border-radius: 12px;
}
@media (max-width: 700px) {
    .block-container { padding: 1rem .8rem 2rem; }
    .hero-banner { border-radius: 16px; }
}
</style>
""", unsafe_allow_html=True)






st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">BIOLOGICAL AGE • HEALTH INSIGHTS</div>
    <h1>BioAge Insight</h1>
    <p class="hero-subtitle">Know Your Body. Beyond Your Years.</p>
    <p class="hero-description">
        Explore how lifestyle, clinical biomarkers, and wearable data
        relate to physiological health.
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "Prototype for educational use. This application does not diagnose "
    "disease or provide a fully validated biological-age measurement."
)
st.markdown(
    "**Explore the prototype:** wearable trends  ·  health profile  ·  clinical PhenoAge  ·  two-person comparison",
    help="For a short demo, show the wearable overview first, then calculate and compare two people, and finish with the personalised next steps."
)


# Example data for demonstration only
data = pd.read_csv("bioage_insight_diverse_synthetic_smartwatch_data.csv")

data["date"] = pd.to_datetime(data["date"])
data["Day"] = data["date"].dt.strftime("%a %d %b")

st.header("📊 Wearable Health Dashboard")
st.caption("A quick view of the sample wearable trends. Sample readings are fictional and for demonstration only.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average resting heart rate",
              f"{data['resting_heart_rate_bpm'].mean():.0f} bpm")

with col2:
    st.metric("Average sleep",
              f"{data['sleep_duration_hours'].mean():.1f} hours")

with col3:
    st.metric("Average daily steps",
              f"{data['steps'].mean():,.0f}")

st.divider()

st.subheader("Weekly Activity")
fig_steps = px.bar(
    data,
    x="Day",
    y="steps",
    title="Daily steps",
    labels={"steps": "Steps", "Day": "Day"}
)
fig_steps.update_traces(hovertemplate="%{x}<br>%{y:,.0f} steps<extra></extra>")
fig_steps.update_layout(
    height=410,
    margin=dict(l=72, r=24, t=65, b=78),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.55)",
    font=dict(family="Arial, sans-serif", size=13, color="#17324d"),
    title=dict(x=0.02, font=dict(size=19, color="#17324d")),
    xaxis=dict(
        title=dict(text="Day", font=dict(size=14, color="#17324d")),
        showgrid=False, showline=True, linecolor="#b7cbd6",
        tickfont=dict(size=12, color="#17324d"),
        tickangle=-35, automargin=True, ticks="outside"
    ),
    yaxis=dict(
        title=dict(text="Steps per day", font=dict(size=14, color="#17324d")),
        gridcolor="#dce8ee", showline=False, zeroline=False,
        tickfont=dict(size=12, color="#17324d"),
        automargin=True, ticks="outside"
    ),
    bargap=0.22
)
st.plotly_chart(fig_steps, use_container_width=True)

chart_col_hr, chart_col_sleep = st.columns(2, gap="large")

with chart_col_hr:
    st.subheader("Resting Heart Rate")
    fig_hr = px.line(
        data,
        x="Day",
        y="resting_heart_rate_bpm",
        markers=True,
        title="Daily resting heart rate",
        labels={"Day": "Day", "resting_heart_rate_bpm": "Heart rate (bpm)"}
    )
    fig_hr.update_traces(line_width=3, marker_size=7, hovertemplate="%{x}<br>%{y:.0f} bpm<extra></extra>")
    fig_hr.update_layout(
        height=370, margin=dict(l=68, r=18, t=62, b=65),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.55)",
        font=dict(family="Arial, sans-serif", size=12, color="#17324d"),
        title=dict(x=0.02, font=dict(size=17, color="#17324d")),
        xaxis=dict(title="Day", showgrid=False, tickfont=dict(size=11, color="#17324d"),
                   tickangle=-30, automargin=True),
        yaxis=dict(title="Heart rate (bpm)", gridcolor="#dce8ee",
                   tickfont=dict(size=11, color="#17324d"), automargin=True)
    )
    st.plotly_chart(fig_hr, use_container_width=True)

with chart_col_sleep:
    st.subheader("Sleep Pattern")
    fig_sleep = px.bar(
        data,
        x="Day",
        y="sleep_duration_hours",
        title="Hours of sleep per day",
        labels={"Day": "Day", "sleep_duration_hours": "Sleep (hours)"}
    )
    fig_sleep.update_traces(marker_line_width=0, hovertemplate="%{x}<br>%{y:.1f} hours<extra></extra>")
    fig_sleep.update_layout(
        height=370, margin=dict(l=68, r=18, t=62, b=65),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.55)",
        font=dict(family="Arial, sans-serif", size=12, color="#17324d"),
        title=dict(x=0.02, font=dict(size=17, color="#17324d")),
        xaxis=dict(title="Day", showgrid=False, tickfont=dict(size=11, color="#17324d"),
                   tickangle=-30, automargin=True),
        yaxis=dict(title="Sleep duration (hours)", gridcolor="#dce8ee",
                   tickfont=dict(size=11, color="#17324d"), automargin=True)
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

with st.expander("View all sample wearable readings", expanded=False):
    st.caption("Fictional demonstration data. Replace with real wearable exports only when you have permission to use them.")
    st.dataframe(data, hide_index=True, use_container_width=True)

st.header("🌿 Health & Lifestyle Assessment")

st.write("Enter additional health information to create a broader health profile.")

with st.expander("Personal and body measurements", expanded=True):
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=160.0, step=1.0)
    weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=60.0, step=1.0)
    waist_cm = st.number_input("Waist circumference (cm)", min_value=30.0, max_value=250.0, value=75.0, step=1.0)

    bmi = weight_kg / ((height_cm / 100) ** 2)
    st.metric("BMI (screening measure)", f"{bmi:.1f}")

with st.expander("Health measurements (if known)"):
    systolic_bp = st.number_input("Systolic blood pressure (mmHg)", min_value=0, max_value=300, value=0)
    diastolic_bp = st.number_input("Diastolic blood pressure (mmHg)", min_value=0, max_value=200, value=0)
    glucose = st.number_input("Blood glucose (mg/dL; enter 0 if unknown)", min_value=0.0, max_value=1000.0, value=0.0)
    cholesterol = st.number_input("Total cholesterol (mg/dL; enter 0 if unknown)", min_value=0.0, max_value=1000.0, value=0.0)

with st.expander("Lifestyle habits"):
    activity = st.selectbox("Physical activity", ["Low", "Moderate", "High"])
    diet = st.selectbox("Typical diet quality", ["Needs improvement", "Mixed", "Balanced"])
    sleep_quality = st.selectbox("Perceived sleep quality", ["Poor", "Fair", "Good"])
    stress = st.selectbox("Usual stress level", ["Low", "Moderate", "High"])
    smoking = st.selectbox("Smoking status", ["Never", "Former", "Current", "Prefer not to say"])
    alcohol = st.selectbox("Alcohol use", ["Never", "Occasionally", "Frequently", "Prefer not to say"])

st.subheader("Health Profile Summary")
st.write(f"**BMI:** {bmi:.1f}")
st.write(f"**Activity:** {activity} | **Diet:** {diet}")
st.write(f"**Sleep quality:** {sleep_quality} | **Stress:** {stress}")
st.caption("This is a preliminary health and lifestyle profile, not a diagnosis or validated biological-age calculation. Enter clinical measurements only when you know them; zero means unknown.")

st.subheader("Your Personalized Health Insights")

insights = []

if bmi >= 30:
    insights.append("Your BMI is in the obesity screening range. Consider discussing your overall health with a healthcare professional.")
elif bmi >= 25:
    insights.append("Your BMI is in the overweight screening range. BMI is only one screening measure and does not assess health on its own.")
elif bmi < 18.5:
    insights.append("Your BMI is in the underweight screening range. Consider discussing your nutritional needs with a healthcare professional.")
else:
    insights.append("Your BMI is within the standard adult screening range. This alone does not confirm overall health.")

if activity == "Low":
    insights.append("Consider gradually increasing physical activity, as appropriate for your health and abilities.")
elif activity == "Moderate":
    insights.append("Maintain regular physical activity and increase it gradually if appropriate.")
else:
    insights.append("Maintain a sustainable activity routine and allow enough time for recovery.")

if sleep_quality == "Poor":
    insights.append("Review your sleep routine and consider seeking advice if poor sleep persists.")

if stress == "High":
    insights.append("Consider practical stress-management strategies and support if stress is affecting daily life.")

if diet == "Needs improvement":
    insights.append("Consider a balanced eating pattern with vegetables, fruits, protein sources, and whole grains.")

for insight in insights:
    st.write("• " + insight)

if systolic_bp > 0 and diastolic_bp > 0:
    st.write(f"Blood pressure entered: {systolic_bp}/{diastolic_bp} mmHg. One reading alone cannot establish a diagnosis.")

if glucose > 0:
    st.write(f"Blood glucose entered: {glucose} mg/dL. Interpretation depends on whether the test was fasting, random, or after a meal.")

if cholesterol > 0:
    st.write(f"Total cholesterol entered: {cholesterol} mg/dL. Discuss results with a healthcare professional for appropriate interpretation.")

st.info(
    "These are preliminary educational insights, not a diagnosis "
    "or a validated biological-age estimate."
)

st.caption("Sample readings below are fictional.")


# --------------------------------------------------
# BIOAGE INSIGHT: PUBLISHED PHENOAGE CALCULATION
# --------------------------------------------------

import math


def calculate_phenoage(
    age,
    albumin_g_l,
    creatinine_umol_l,
    glucose_mmol_l,
    crp_mg_dl,
    lymphocyte_percent,
    mcv_fl,
    rdw_percent,
    alp_u_l,
    wbc_10e9_l,
):
    #Calculate clinical PhenoAge using published coefficients.

    values = [
        age, albumin_g_l, creatinine_umol_l, glucose_mmol_l,
        crp_mg_dl, lymphocyte_percent, mcv_fl, rdw_percent,
        alp_u_l, wbc_10e9_l
    ]

    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("All inputs must be finite numbers.")

    if age <= 0 or albumin_g_l <= 0 or creatinine_umol_l <= 0:
        raise ValueError("Age, albumin and creatinine must be positive.")

    if glucose_mmol_l <= 0 or crp_mg_dl <= 0:
        raise ValueError("Glucose and CRP must be positive.")

    if not 0 <= lymphocyte_percent <= 100:
        raise ValueError("Lymphocyte percentage must be between 0 and 100.")

    if min(mcv_fl, rdw_percent, alp_u_l, wbc_10e9_l) <= 0:
        raise ValueError("MCV, RDW, ALP and WBC must be positive.")

    xb = (
        -19.907
        - 0.0336 * albumin_g_l
        + 0.0095 * creatinine_umol_l
        + 0.1953 * glucose_mmol_l
        + 0.0954 * math.log(crp_mg_dl)
        - 0.0120 * lymphocyte_percent
        + 0.0268 * mcv_fl
        + 0.3306 * rdw_percent
        + 0.00188 * alp_u_l
        + 0.0554 * wbc_10e9_l
        + 0.0804 * age
    )

    # Algebraically equivalent form of the published equation.
    phenoage = (
        141.50225
        + (
            math.log(0.00553 * 1.51714 / 0.0076927)
            + xb
        ) / 0.090165
    )

    if not math.isfinite(phenoage) or phenoage < 0:
        raise ValueError(
            "The calculation produced an invalid result. "
            "Check the laboratory values and units."
        )

    return phenoage

# --------------------------------------------------
# PHENOAGE INPUT FORM
# --------------------------------------------------

st.header("🧬 Clinical Biological Age")
st.write(
    "Enter laboratory results to calculate a preliminary "
    "clinical PhenoAge estimate."
)
with st.form("phenoage_form"):
    st.subheader("Enter laboratory results")

    pheno_age_years = st.number_input(
        "Chronological age (years)", min_value=1, max_value=120, value=30
    )

    albumin = st.number_input("Albumin (g/L)", min_value=0.0, value=0.0)
    creatinine = st.number_input("Creatinine (µmol/L)", min_value=0.0, value=0.0)
    glucose_pheno = st.number_input("Glucose (mmol/L)", min_value=0.0, value=0.0)
    crp = st.number_input("CRP (mg/dL)", min_value=0.0, value=0.0)
    lymphocytes = st.number_input(
        "Lymphocyte percentage (%)", min_value=0.0, max_value=100.0, value=0.0
    )
    mcv = st.number_input("MCV (fL)", min_value=0.0, value=0.0)
    rdw = st.number_input("RDW (%)", min_value=0.0, value=0.0)
    alp = st.number_input("Alkaline phosphatase (U/L)", min_value=0.0, value=0.0)
    wbc = st.number_input("White blood cell count (10⁹/L)", min_value=0.0, value=0.0)

    calculate_button = st.form_submit_button("Calculate PhenoAge")

if calculate_button:
    try:
        result = calculate_phenoage(
            age=pheno_age_years,
            albumin_g_l=albumin,
            creatinine_umol_l=creatinine,
            glucose_mmol_l=glucose_pheno,
            crp_mg_dl=crp,
            lymphocyte_percent=lymphocytes,
            mcv_fl=mcv,
            rdw_percent=rdw,
            alp_u_l=alp,
            wbc_10e9_l=wbc,
        )

        st.metric("Estimated PhenoAge", f"{result:.1f} years")
        difference = result - pheno_age_years
        st.write(f"Difference from chronological age: {difference:+.1f} years")
        st.caption(
            "Research-derived estimate, not a diagnosis or a complete measure "
            "of biological aging. Use actual laboratory results and their "
            "reported units; zero values are not valid substitutes for missing tests."
        )

    except ValueError as error:
        st.error(str(error))


# --------------------------------------------------
# COMPARE TWO PEOPLE
# --------------------------------------------------

st.divider()
st.header("👥 Side-by-Side Biological Age Comparison")
st.write(
    
    "Compare two people using their clinical PhenoAge estimates. "
    "Same-Age Comparison focuses on people of the same chronological age; "
    "Flexible Comparison also allows different ages."

)

comparison_mode = st.radio(
    "Choose comparison mode",
    ["Same-Age Comparison", "Flexible Comparison"],
    horizontal=True,
    key="comparison_mode",
)


# Side-by-side comparison workspace
with st.form("compare_phenoage_form"):
    st.markdown(
        '<div class="section-intro"><strong>Compare two health profiles</strong><br>'
        'Enter both people side by side. Use the same chronological age to focus on biomarker differences, '
        'or choose Flexible Comparison to compare different ages.</div>',
        unsafe_allow_html=True
    )

    sector_options = ["IT / Software", "Clinical Laboratory", "Mining", "Other"]
    person_a_col, person_b_col = st.columns(2, gap="large")

    with person_a_col:
        st.markdown('<div class="person-card-a">', unsafe_allow_html=True)
        st.markdown("### 🟦 Person A")
        st.caption("Profile A · Teal")
        sector_a = st.selectbox("Occupational sector", sector_options, key="sector_a")
        age_a = st.number_input(
            "Chronological age (years)", min_value=1, max_value=120, value=30, key="age_a"
        )
        st.markdown("**Clinical biomarkers**")
        albumin_a = st.number_input("Albumin (g/L)", min_value=0.0, value=0.0, key="albumin_a")
        creatinine_a = st.number_input("Creatinine (µmol/L)", min_value=0.0, value=0.0, key="creatinine_a")
        glucose_a = st.number_input("Glucose (mmol/L)", min_value=0.0, value=0.0, key="glucose_a")
        crp_a = st.number_input("CRP (mg/dL)", min_value=0.0, value=0.0, key="crp_a")
        lymphocytes_a = st.number_input("Lymphocyte percentage (%)", min_value=0.0, max_value=100.0, value=0.0, key="lymphocytes_a")
        mcv_a = st.number_input("MCV (fL)", min_value=0.0, value=0.0, key="mcv_a")
        rdw_a = st.number_input("RDW (%)", min_value=0.0, value=0.0, key="rdw_a")
        alp_a = st.number_input("Alkaline phosphatase (U/L)", min_value=0.0, value=0.0, key="alp_a")
        wbc_a = st.number_input("White blood cell count (10⁹/L)", min_value=0.0, value=0.0, key="wbc_a")
        st.markdown('</div>', unsafe_allow_html=True)

    with person_b_col:
        st.markdown('<div class="person-card-b">', unsafe_allow_html=True)
        st.markdown("### 🟪 Person B")
        st.caption("Profile B · Violet")
        sector_b = st.selectbox("Occupational sector", sector_options, index=1, key="sector_b")
        age_b = st.number_input(
            "Chronological age (years)", min_value=1, max_value=120, value=30, key="age_b"
        )
        st.markdown("**Clinical biomarkers**")
        albumin_b = st.number_input("Albumin (g/L)", min_value=0.0, value=0.0, key="albumin_b")
        creatinine_b = st.number_input("Creatinine (µmol/L)", min_value=0.0, value=0.0, key="creatinine_b")
        glucose_b = st.number_input("Glucose (mmol/L)", min_value=0.0, value=0.0, key="glucose_b")
        crp_b = st.number_input("CRP (mg/dL)", min_value=0.0, value=0.0, key="crp_b")
        lymphocytes_b = st.number_input("Lymphocyte percentage (%)", min_value=0.0, max_value=100.0, value=0.0, key="lymphocytes_b")
        mcv_b = st.number_input("MCV (fL)", min_value=0.0, value=0.0, key="mcv_b")
        rdw_b = st.number_input("RDW (%)", min_value=0.0, value=0.0, key="rdw_b")
        alp_b = st.number_input("Alkaline phosphatase (U/L)", min_value=0.0, value=0.0, key="alp_b")
        wbc_b = st.number_input("White blood cell count (10⁹/L)", min_value=0.0, value=0.0, key="wbc_b")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    compare_button = st.form_submit_button("🧬  Calculate & Compare Profiles", use_container_width=True)

if compare_button:
    
    if comparison_mode == "Same-Age Comparison" and age_a != age_b:
        st.warning(
            "Enter the same chronological age for both people "
            "in Same-Age Comparison mode."
        )
    else:
        
        
        try:
            if min(
                albumin_a, creatinine_a, glucose_a, crp_a,
                mcv_a, rdw_a, alp_a, wbc_a,
                albumin_b, creatinine_b, glucose_b, crp_b,
                mcv_b, rdw_b, alp_b, wbc_b
            ) <= 0:
                raise ValueError("Enter valid, non-zero laboratory results for both people.")

            result_a = calculate_phenoage(
                age_a, albumin_a, creatinine_a, glucose_a, crp_a,
                lymphocytes_a, mcv_a, rdw_a, alp_a, wbc_a
            )
            result_b = calculate_phenoage(
                age_b, albumin_b, creatinine_b, glucose_b, crp_b,
                lymphocytes_b, mcv_b, rdw_b, alp_b, wbc_b
            )

            result_col_a, result_delta, result_col_b = st.columns(3, gap="large")
            with result_col_a:
                st.metric(f"🟦 Person A · {sector_a}", f"{result_a:.1f} years",
                          delta=f"{result_a - age_a:+.1f} vs chronological age")
            with result_delta:
                st.metric("↔ Difference", f"{abs(result_a - result_b):.1f} years")
            with result_col_b:
                st.metric(f"🟪 Person B · {sector_b}", f"{result_b:.1f} years",
                          delta=f"{result_b - age_b:+.1f} vs chronological age")

            st.divider()
            st.subheader("🌿 Personalised next steps")

            higher_person = (
                "Person A" if result_a > result_b
                else "Person B" if result_b > result_a
                else None
            )

            if higher_person is None:
                st.info(
                    "Both people have the same estimated PhenoAge in this calculation. "
                    "The general healthy-habit suggestions below can help both people."
                )
                higher_sector = None
                higher_gap = 0
            else:
                higher_sector = sector_a if higher_person == "Person A" else sector_b
                higher_gap = (
                    result_a - age_a if higher_person == "Person A"
                    else result_b - age_b
                )
                st.markdown(
                    f"**{higher_person} ({higher_sector}) has the higher estimated PhenoAge.** "
                    "Use this result as a prompt to review health information—not as a diagnosis "
                    "or proof that occupation caused the difference."
                )

            habit_col, followup_col = st.columns(2, gap="large")
            with habit_col:
                with st.container(border=True):
                    st.markdown("### 🌱 Everyday habits")
                    st.markdown(
                        """
                        - **Movement:** Build up gradually towards regular moderate physical activity.
                        - **Sleep:** Keep a consistent sleep and wake time, and aim for sufficient sleep.
                        - **Food:** Choose a varied diet with vegetables, fruit, pulses, whole grains, nuts and suitable protein.
                        - **Tobacco:** Avoid smoking and other tobacco products; seek support to quit if needed.
                        - **Stress:** Take regular breaks and make time for relaxing activities and social support.
                        """
                    )

            with followup_col:
                with st.container(border=True):
                    st.markdown("### 🩺 Health follow-up")
                    st.markdown(
                        """
                        - **Check the report:** Confirm units and reference ranges, and note whether testing happened during an illness.
                        - **Talk to a clinician:** Ask about out-of-range glucose, CRP, blood counts, albumin or creatinine.
                        - **Consider work exposures:** Discuss relevant workplace risks and protective measures with an occupational-health professional.
                        - **Repeat tests only when advised:** Do not change or manipulate lab values to chase a lower score.
                        - **Review over time:** Use professional guidance to decide whether follow-up measurements are appropriate.
                        """
                    )

            if higher_person is not None:
                st.caption(
                    f"Difference between {higher_person}'s estimated PhenoAge and chronological age: "
                    f"{higher_gap:+.1f} years. PhenoAge is an estimate, not a diagnosis; "
                    "lifestyle changes do not guarantee a lower score."
                )
            else:
                st.caption(
                    "PhenoAge is an estimate, not a diagnosis. These general suggestions are educational "
                    "and do not guarantee a lower score."
                )

            st.subheader("PhenoAge Comparison")

            chart_data = pd.DataFrame({
                "Person": ["Person A", "Person B"],
                "Chronological Age": [age_a, age_b],
                "Estimated PhenoAge": [result_a, result_b],
            })

            comparison_fig = px.bar(
                chart_data.melt(
                    id_vars="Person",
                    value_vars=["Chronological Age", "Estimated PhenoAge"],
                    var_name="Measure",
                    value_name="Age (years)"
                ),
                x="Person", y="Age (years)", color="Measure", barmode="group",
                title="Chronological age vs estimated PhenoAge",
                color_discrete_sequence=["#087f8c", "#7565d8"],
                text_auto=".1f"
            )
            comparison_fig.update_layout(
                height=390,
    margin=dict(l=65, r=25, t=65, b=65),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", size=14, color="#17324d"),
    legend=dict(
        title_text="",
        font=dict(size=14, color="#17324d")
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=15, color="#17324d"),
        title_font=dict(size=15, color="#17324d"),
        automargin=True
    ),
    yaxis=dict(
        gridcolor="#dce8ee",
        tickfont=dict(size=13, color="#17324d"),
        title_font=dict(size=14, color="#17324d"),
        automargin=True
    ),
    title_x=0.02
            )
            st.plotly_chart(comparison_fig, use_container_width=True)

            comparison = {
                "Measurement": [
                    "Chronological age", "Albumin", "Creatinine",
                    "Glucose", "CRP", "Lymphocyte percentage",
                    "MCV", "RDW", "Alkaline phosphatase", "WBC"
                ],
                "Person A": [
                    age_a, albumin_a, creatinine_a, glucose_a, crp_a,
                    lymphocytes_a, mcv_a, rdw_a, alp_a, wbc_a
                ],
                "Person B": [
                    age_b, albumin_b, creatinine_b, glucose_b, crp_b,
                    lymphocytes_b, mcv_b, rdw_b, alp_b, wbc_b
                ]
            }
            st.subheader("Clinical measurements compared")
            st.dataframe(comparison, hide_index=True, use_container_width=True)
            
            st.subheader("Why are their results different?")

            biomarker_notes = [
                ("Albumin", albumin_a, albumin_b,
                 "A protein influenced by nutrition, liver function, kidney function and inflammation."),
                ("Creatinine", creatinine_a, creatinine_b,
                 "Interpretation depends on kidney function, muscle mass and other factors."),
                ("Glucose", glucose_a, glucose_b,
                 "Interpretation depends on fasting status, recent meals and the laboratory reference range."),
                ("CRP", crp_a, crp_b,
                 "A marker of inflammation; infections and many other conditions can affect it."),
                ("Lymphocyte percentage", lymphocytes_a, lymphocytes_b,
                 "Interpret alongside the total white blood cell count and clinical context."),
                ("MCV", mcv_a, mcv_b,
                 "Reflects average red blood cell size and may need interpretation with other blood results."),
                ("RDW", rdw_a, rdw_b,
                 "Reflects variation in red blood cell size and is interpreted with the rest of the blood count."),
                ("Alkaline phosphatase", alp_a, alp_b,
                 "Can be influenced by liver, bile duct and bone conditions."),
                ("White blood cell count", wbc_a, wbc_b,
                 "Can vary with infections, inflammation, medicines and other factors."),
            ]

            explanation_rows = []

            for marker, value_a, value_b, note in biomarker_notes:
                if value_a > value_b:
                    difference = "Higher in Person A"
                elif value_b > value_a:
                    difference = "Higher in Person B"
                else:
                    difference = "Same value"

                explanation_rows.append({
                    "Biomarker": marker,
                    "Person A": value_a,
                    "Person B": value_b,
                    "Comparison": difference,
                    "What it may indicate": note,
                })

            with st.expander("Explore each clinical biomarker", expanded=False):
                st.dataframe(
                    explanation_rows,
                    hide_index=True,
                    use_container_width=True
                )

            st.info(
                "These differences help identify which laboratory results "
                "to review. A higher or lower value is not automatically "
                "better or worse, and this table does not establish what "
                "caused the difference in estimated PhenoAge."
            )
            
            st.subheader("Understanding the difference")

            st.write(
                "PhenoAge estimates are calculated using a combination "
                "of chronological age and nine laboratory biomarkers."
            )

            st.write(
                "Differences in albumin, creatinine, glucose, CRP, "
                "lymphocyte percentage, MCV, RDW, alkaline phosphatase "
                "and white blood cell count can influence the estimate."
            )

            st.info(
                "The model combines these measurements mathematically. "
                "This comparison does not prove that a person's occupation "
                "caused the difference or identify a medical diagnosis."
            )

            contribution_rows = [
                {"Biomarker": "Albumin", "A → B contribution": -0.0336 * (albumin_a - albumin_b)},
                {"Biomarker": "Creatinine", "A → B contribution": 0.0095 * (creatinine_a - creatinine_b)},
                {"Biomarker": "Glucose", "A → B contribution": 0.1953 * (glucose_a - glucose_b)},
                {"Biomarker": "CRP", "A → B contribution": 0.0954 * (math.log(crp_a) - math.log(crp_b))},
                {"Biomarker": "Lymphocyte percentage", "A → B contribution": -0.0120 * (lymphocytes_a - lymphocytes_b)},
                {"Biomarker": "MCV", "A → B contribution": 0.0268 * (mcv_a - mcv_b)},
                {"Biomarker": "RDW", "A → B contribution": 0.3306 * (rdw_a - rdw_b)},
                {"Biomarker": "Alkaline phosphatase", "A → B contribution": 0.00188 * (alp_a - alp_b)},
                {"Biomarker": "White blood cell count", "A → B contribution": 0.0554 * (wbc_a - wbc_b)},
                {"Biomarker": "Chronological age", "A → B contribution": 0.0804 * (age_a - age_b)},
            ]
            
            st.caption(
                "A − B contribution = the biomarker's contribution to the "
                "difference in the intermediate linear predictor. Positive "
                "values push that predictor higher for Person A; negative "
                "values push it higher for Person B. These are not years of "
                "ageing. The final PhenoAge transformation is nonlinear."
            )
            with st.expander("View biomarker contribution table and chart", expanded=False):
                contribution_df = pd.DataFrame(contribution_rows)
                st.dataframe(
                    contribution_df.sort_values("A → B contribution", ascending=False),
                    hide_index=True,
                    use_container_width=True
                )
                contribution_fig = px.bar(
                    contribution_df.sort_values("A → B contribution"),
                    x="A → B contribution",
                    y="Biomarker",
                    orientation="h",
                    title="Contribution to intermediate model score (A − B)",
                    labels={"A → B contribution": "Model-score contribution"}
                )
                contribution_fig.update_layout(
                    height=420, margin=dict(l=12, r=12, t=55, b=12),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#17324d"), title_x=0.02,
                    xaxis=dict(gridcolor="#e7eef3"), yaxis=dict(showgrid=False)
                )
                st.plotly_chart(contribution_fig, use_container_width=True)


            st.subheader("Health factors to review")

            st.markdown(
                "- **Glucose:** Discuss persistently abnormal results with "
                "a healthcare professional; interpret them using the correct "
                "fasting status and laboratory range.\n"
                "- **CRP:** If elevated, a clinician can help assess possible "
                "inflammation or other causes.\n"
                "- **Albumin and creatinine:** Review abnormal results with "
                "a clinician rather than trying to change these values directly.\n"
                "- **MCV, RDW and blood cell counts:** Ask a healthcare "
                "professional whether the results warrant further evaluation.\n"
                "- **General health:** Regular physical activity, adequate "
                "sleep, balanced nutrition and avoiding smoking support "
                "overall health, but do not guarantee a lower biological-age estimate."
            )


            st.caption(
                "Research-derived estimates, not diagnoses. Use valid laboratory "
                "results and correct units. This comparison does not establish "
                "the cause of any age difference."
            )

        except ValueError as error:
            st.error(str(error))

  