# 🏔️ J&K Census 2011 — District Dashboard

An interactive Streamlit dashboard for exploring **Census 2011 district-level data** for Jammu & Kashmir across 22 districts.

## 📊 Dashboard Features

- **KPI Summary Cards** — Total population, literacy rate, sex ratio, urban share, worker participation
- **District-wise Bar Chart** — Any metric, colour-coded by Division (Kashmir / Jammu / Ladakh)
- **Urban vs Rural Donut Charts** — Population split and division-level shares
- **Male vs Female Literacy Grouped Bar** — Gender gap comparison across districts
- **Sex Ratio & Child Sex Ratio Trend** — Both overlaid with national average line
- **Scatter Plot** — Literacy Rate vs Population Density, bubble sized by population
- **Main vs Marginal Workers** — Stacked bar chart
- **Population Treemap** — Division → District hierarchy, coloured by literacy
- **Data Table** — Styled with conditional formatting + gradient highlights
- **Download Buttons** — Filtered CSV, Filtered Excel (with Summary sheet), Full CSV

## 📁 Project Structure

```
jk_census_dashboard/
├── app.py                  # Main Streamlit application
├── data.py                 # Census 2011 data module (22 districts)
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .streamlit/
    └── config.toml         # Theme configuration
```

## 🚀 Run Locally

```bash
# 1. Clone or download this folder
cd jk_census_dashboard

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

The app opens at **http://localhost:8501**

## ☁️ Deploy on Streamlit Community Cloud

1. Push this folder to a **GitHub repository** (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Set:
   - **Repository**: `your-username/your-repo`
   - **Branch**: `main`
   - **Main file path**: `jk_census_dashboard/app.py`
4. Click **Deploy** — live in ~2 minutes ✅

## 📦 Data Coverage

All figures are from **Census of India 2011**:

| Category | Metrics |
|---|---|
| **Population** | Total, Male, Female, Households, Area, Density |
| **Urban/Rural** | Urban population, Rural population, % urban, % rural |
| **Literacy** | Overall, Male, Female literacy rates, Gender gap |
| **Workforce** | Total workers, Main workers, Marginal workers, WPR |
| **Demographics** | Sex ratio (overall & child 0-6), Child sex ratio |

**Source**: censusindia.gov.in — Primary Census Abstract (PCA), District Census Handbook (DCHB)

## 🗂️ District Coverage (22 Districts)

| Division | Districts |
|---|---|
| **Kashmir** | Anantnag, Bandipore, Baramulla, Budgam, Ganderbal, Kulgam, Kupwara, Pulwama, Shopian, Srinagar |
| **Jammu** | Doda, Jammu, Kathua, Kishtwar, Poonch, Rajouri, Ramban, Reasi, Samba, Udhampur |
| **Ladakh** | Kargil, Leh |

---
Built with ❤️ using [Streamlit](https://streamlit.io) · [Plotly](https://plotly.com)
