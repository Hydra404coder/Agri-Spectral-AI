Agri-Spectral-AI

AgriSpectral AI is a software-only fruit quality detection system that emulates AS7265x spectral sensors using open hyperspectral datasets to predict apple freshness, spoilage risk, and pesticide residues.

🚀 Features

Emulates an 18-band AS7265x sensor (wavelengths ~410-940 nm) from mock/hyperspectral data

Freshness Detection via dry-matter percentage analysis

Spoilage Risk Assessment for early degradation detection (Low / Medium / High)

Pesticide Residue Classification (Pure / Fungicide / Insecticide)

Interactive visualizations: spectral charts, PCA, scatter plots, histograms

Professionally styled dashboard built using Streamlit + Plotly + Scikit-learn

Mock sample mode and real-time simulated analytics

📁 Repository Contents
File / Folder	Description
app.py	Main Streamlit application with dashboard logic and visualizations
requirements.txt	Python package dependencies needed to run the dashboard
README.md	This file
💻 Setup & Installation

Clone the repository

git clone https://github.com/Hydra404coder/Agri-Spectral-AI.git
cd Agri-Spectral-AI


Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Run the dashboard

streamlit run app.py

🛠 Usage

Upon startup, the dashboard will generate mock data and display interactive KPIs for freshness, spoilage risk, and pesticide status.

Use the sidebar to select sample threshold, pick sample, and toggle advanced analytics.

Explore spectral lines, PCA visualization, and distributions for insights.

🧪 Tech Stack

Python

Streamlit — for the web dashboard interface

Plotly — interactive charts and plots

Scikit-learn — regression & analysis (e.g. Ridge, PCA)

NumPy / Pandas — data manipulation

✅ Contribution

This repository is currently a demo / prototype. Ideas for extension:

Add real hyperspectral data and sensor calibration

Incorporate gauge‐style visual components & animations

Allow multi-sample or time series comparison

Add export (PDF / CSV) and report generation

Improve responsiveness and design polish

📜 License & Contact

Feel free to use / modify.
Created by Hydra404coder.
