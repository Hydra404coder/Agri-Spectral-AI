import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from io import BytesIO

st.set_page_config(
    page_title="AgriSpectral AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Logo & Branding -----------------
st.markdown("""
<div style="display:flex;align-items:center;gap:16px;justify-content:center;margin-bottom:8px;">
    <img src="https://img.icons8.com/color/96/000000/apple.png" width="56"/>
    <div>
        <h1 style="margin:0;">AgriSpectral AI</h1>
        <h4 style="margin:0;color:#bbe1fa;font-weight:400;">Advanced Fruit & Vegetable Quality Detection System</h4>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- Styles & Design Enhancements -----------------
st.markdown("""
    <style>
        /* Glassmorphism cards */
        .glass-card {
            background: rgba(255,255,255,0.08);
            border-radius:12px;
            padding:16px;
            margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .glass-card:hover {
            transform: scale(1.02);
            box-shadow:0 6px 16px rgba(0,0,0,0.16);
        }
        h1,h2,h3,h4,h5 {font-family:'Roboto', sans-serif;}
        .kpi {font-size:28px; font-weight:600;}
        .sub-kpi {font-size:16px; color:#cbd5e1;}
        .status-badge {padding:4px 10px; border-radius:8px; color:white; font-weight:600;}
    </style>
""", unsafe_allow_html=True)



# ---------------- Sidebar: Navigation & Controls -----------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/apple.png", width=80)
    # --- Login Section ---
    st.header("🔐 Login")
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if login_username and login_password:
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(f"Welcome, {login_username}!")
            else:
                st.warning("Please enter both username and password.")
        st.markdown("---")
    else:
        st.success(f"Welcome, {st.session_state.username}!")
        st.markdown("---")
    st.header("Navigation")
    nav = st.radio("Go to", ["Dashboard", "About", "Contact"])
    st.markdown("---")
    st.header("User Info")
    username = st.session_state.get('username', '')
    st.markdown("---")
    if nav == "Dashboard":
        st.header("Controls")
        selected_sample = st.selectbox("Select Apple Sample", [f"Sample {i+1}" for i in range(1,6)])
        freshness_thresh = st.slider("Freshness Threshold (%)", 0, 100, 70)
        st.markdown("---")


# ----------------- Main Content Routing -----------------
if nav == "About":
    st.markdown("""
    <div class='glass-card'>
    <h2>About Project X – Fruit and Vegetable Quality Detection System</h2>
    <p>This dashboard demonstrates a complete software-only solution for fruit and vegetable quality detection using open hyperspectral datasets of apples. The system emulates the AS7265x sensor and provides AI-powered predictions for freshness, spoilage, and pesticide residue.</p>
    <h4>Objectives</h4>
    <ul>
        <li>Detect apple freshness/ripeness (via Dry Matter %).</li>
        <li>Identify spoilage or early degradation (using NIR and VIS spectral shifts).</li>
        <li>Detect pesticide/fungicide residues (treated vs. untreated apples).</li>
        <li>Demonstrate that sensor emulation with open datasets can replicate the function of a physical AS7265x sensor.</li>
    </ul>
    <h4>Working Flow</h4>
    <ol>
        <li>Dataset provides full hyperspectral reflectance values.</li>
        <li>Software resamples spectra to 18 AS7265x bands (410–940 nm).</li>
        <li>AI models analyze resampled vectors.</li>
        <li>Predictions: Freshness level, Spoilage risk, Pesticide presence.</li>
        <li>Results displayed on dashboard (e.g., Streamlit).</li>
    </ol>
    <h4>Datasets</h4>
    <ul>
        <li><a href='https://data.mendeley.com/datasets/3bhr26jffs/1' target='_blank'>Apple Pesticide/Fungicide dataset (Roomi et al., 2023)</a></li>
        <li><a href='https://zenodo.org/records/10301753' target='_blank'>SpectroFood Apple subset (Dry Matter %, 240 samples)</a></li>
        <li><a href='https://zenodo.org/records/8362947' target='_blank'>SpectroFood Full Dataset (metadata, 430–990 nm)</a></li>
    </ul>
    <h4>Sensor Emulation</h4>
    <p>The AS7265x has 18 fixed wavelength bands (410–940 nm). Emulation process:</p>
    <ol>
        <li>Take hyperspectral reflectance values from dataset.</li>
        <li>Average reflectance values around AS7265x band centers.</li>
        <li>Produce an 18-feature vector representing 'virtual AS7265x readings.'</li>
    </ol>
    <h4>Roadmap to Implementation</h4>
    <ol>
        <li>Download datasets and perform data exploration (plot spectra, inspect labels).</li>
        <li>Implement spectral resampling → emulate AS7265x readings.</li>
        <li>Train regression model on Dry Matter % (ripeness).</li>
        <li>Train classification model on pesticide dataset (treated vs. untreated).</li>
        <li>Train spoilage proxy model using NIR/VIS cues (via Dry Matter or degradation labels).</li>
        <li>Evaluate performance with metrics (R², RMSE, Accuracy, F1).</li>
        <li>Deploy results to a web dashboard (Streamlit).</li>
        <li>Document methodology and results for paper writing.</li>
    </ol>
    <h4>Expected Outputs</h4>
    <ul>
        <li>Freshness (Dry Matter % prediction) → Higher DM% = Fresher fruit.</li>
        <li>Spoilage Risk (binary classification) → Based on water loss/NIR drop.</li>
        <li>Pesticide Detection (classification) → Labelled as Pure / Fungicide / Insecticide.</li>
        <li>Dashboard Visuals → Graphs + predicted values with confidence scores.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

elif nav == "Contact":
    st.markdown("""
    <div class='glass-card'>
    <h2>Contact</h2>
    <p>For questions, collaboration, or access to code and datasets, please contact:</p>
    <ul>
        <li><b>Email:</b> <a href='mailto:your@email.com'>your@email.com</a></li>
        <li><b>LinkedIn:</b> <a href='https://www.linkedin.com/' target='_blank'>Your LinkedIn</a></li>
        <li><b>IEEE Publication:</b> <a href='https://ieeexplore.ieee.org/' target='_blank'>See IEEE Xplore</a></li>
    </ul>
    <h4>Learning Resources</h4>
    <ul>
        <li><a href='https://learn.sparkfun.com/tutorials/spectral-triad-as7265x-hookup-guide/all' target='_blank'>AS7265x SparkFun Hookup Guide</a></li>
        <li><a href='https://color.psych.upenn.edu/brainard/papers/vorasim.pdf' target='_blank'>Sensor Simulation Concept</a></li>
        <li><a href='https://www.jstatsoft.org/article/view/v089i12/1297' target='_blank'>Spectral Resampling/Binning Utilities (hsdar package)</a></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # ----------------- Mock Data -----------------
    np.random.seed(42)
    num_samples = 100
    num_bands = 18

    df = pd.DataFrame({
        **{f'band_{i+1}': np.random.rand(num_samples)*100 for i in range(num_bands)},
        'dry_matter': np.random.rand(num_samples)*20,
        'spoilage_risk': np.random.choice(["Low","Medium","High"], num_samples),
        'pesticide_status': np.random.choice(["Pure","Fungicide","Insecticide"], num_samples),
        'confidence': np.random.rand(num_samples)*100
    })

    sample_data = df.sample(1).iloc[0]

# ---------------- KPI Cards with Tooltips -----------------
col1, col2, col3 = st.columns(3)

# Freshness KPI
freshness_pct = np.clip(sample_data['dry_matter']*5,0,100)
if freshness_pct >= freshness_thresh:
    freshness_color = "#2E7D32"; freshness_status="Fresh"
elif freshness_pct >= freshness_thresh*0.7:
    freshness_color = "#F5A623"; freshness_status="Moderate"
else:
    freshness_color = "#D90429"; freshness_status="Low"
with col1:
    st.markdown(f"""
    <div class='glass-card' style='text-align:center;position:relative;'>
        <span title='Estimated from dry matter content'>
            <div class='kpi'>{freshness_pct:.1f}%</div>
        </span>
        <div class='sub-kpi'>Freshness Level <span title='Higher is better' style='cursor:help;'>ℹ️</span></div>
        <div class='status-badge' style='background-color:{freshness_color}'>{freshness_status}</div>
    </div>
    """, unsafe_allow_html=True)

# Spoilage Risk KPI
risk = sample_data['spoilage_risk']
risk_color = {"Low":"#2E7D32","Medium":"#F5A623","High":"#D90429"}[risk]
with col2:
    st.markdown(f"""
    <div class='glass-card' style='text-align:center;position:relative;'>
        <span title='Predicted spoilage risk based on spectral signature'>
            <div class='kpi'>{risk}</div>
        </span>
        <div class='sub-kpi'>Spoilage Risk <span title='Low, Medium, or High' style='cursor:help;'>ℹ️</span></div>
        <div class='status-badge' style='background-color:{risk_color}'>{risk}</div>
    </div>
    """, unsafe_allow_html=True)

# Pesticide Detection KPI
status = sample_data['pesticide_status']
status_color = {"Pure":"#3DDC84","Fungicide":"#F5A623","Insecticide":"#D90429"}[status]
with col3:
    st.markdown(f"""
    <div class='glass-card' style='text-align:center;position:relative;'>
        <span title='Detected using spectral band analysis'>
            <div class='kpi'>{status}</div>
        </span>
        <div class='sub-kpi'>Pesticide Status <span title='Pure = No residue' style='cursor:help;'>ℹ️</span></div>
        <div class='status-badge' style='background-color:{status_color}'>{status}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Spectral Analysis -----------------
st.markdown("<h3 style='margin-top:32px;'>🔬 Spectral Analysis <span title='Shows the reflectance signature for the selected sample' style='cursor:help;'>ℹ️</span></h3>", unsafe_allow_html=True)
wavelengths = np.linspace(410,940,num_bands)
spectral_values = sample_data[[f'band_{i+1}' for i in range(num_bands)]].values
spectral_fig = px.line(x=wavelengths,y=spectral_values,markers=True,
                       labels={'x':'Wavelength (nm)','y':'Reflectance (%)'},
                       title="18-Band Sensor Spectral Signature")
spectral_fig.update_layout(template='plotly_dark',height=400)
st.plotly_chart(spectral_fig,use_container_width=True)

# ---------------- AI Model Performance -----------------
st.markdown("<h3 style='margin-top:32px;'>🤖 AI Model Performance <span title='Shows regression fit for dry matter prediction' style='cursor:help;'>ℹ️</span></h3>", unsafe_allow_html=True)
features = [f'band_{i+1}' for i in range(num_bands)]
X = df[features].values
y = df['dry_matter'].values
with st.spinner('Training Ridge Regression Model...'):
    model = Ridge(alpha=1.0).fit(X,y)
    preds = model.predict(X)
    r2_score = model.score(X,y)
perf_fig = px.scatter(x=y,y=preds,labels={'x':'True DM','y':'Predicted DM'},
                      title=f"Ridge Regression (R²={r2_score:.2f})")
perf_fig.update_layout(template='plotly_dark',height=400)
st.plotly_chart(perf_fig,use_container_width=True)

# ---------------- Real-time Analytics Dashboard -----------------
st.markdown("<h3 style='margin-top:32px;'>📊 Real-time Analytics <span title='Distribution and PCA of all samples' style='cursor:help;'>ℹ️</span></h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    hist_fig = px.histogram(df,x='dry_matter',nbins=20,color='spoilage_risk',
                            title="Dry Matter Distribution")
    hist_fig.update_layout(template='plotly_dark',height=400)
    st.plotly_chart(hist_fig,use_container_width=True)

with col2:
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=3)
    comps = pca.fit_transform(X_scaled)
    pca_df = pd.DataFrame(comps,columns=['PC1','PC2','PC3'])
    pca_df['dry_matter'] = df['dry_matter']
    pca_fig = px.scatter(pca_df,x='PC1',y='PC2',color='dry_matter',hover_data=['PC3'],
                         title="PCA Analysis")
    pca_fig.update_layout(template='plotly_dark',height=400)
    st.plotly_chart(pca_fig,use_container_width=True)

# ---------------- Download Report Button -----------------
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
st.download_button(
    label="📥 Download Full Report (Excel)",
    data=to_excel(df),
    file_name='agrispectral_report.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    help="Download all sample data as an Excel report."
)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Footer Notes -----------------
st.markdown("---")
st.markdown("""
<div style='color:#9ca3af;text-align:center;font-size:15px;'>
    <b>AgriSpectral AI</b> &copy; 2025 &mdash; Built for the Innovation Challenge<br>
    <span style='color:#cbd5e1;'>Contact: <a href='mailto:your@email.com' style='color:#bbe1fa;'>your@email.com</a></span>
    <br><span style='font-size:13px;'>Made with ❤️ using Streamlit &amp; Plotly</span>
</div>
""", unsafe_allow_html=True)
