import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from data import get_district_data

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="J&K Census 2011 Dashboard",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2rem; font-weight: 700; color: #01696f;
        border-bottom: 3px solid #01696f; padding-bottom: 0.5rem; margin-bottom: 1rem;
    }
    .kpi-box {
        background: linear-gradient(135deg, #f7f6f2 0%, #e6f4f4 100%);
        border-left: 4px solid #01696f; border-radius: 8px;
        padding: 1rem 1.2rem; margin: 0.3rem 0;
    }
    .kpi-label { font-size: 0.75rem; color: #7a7974; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { font-size: 1.6rem; font-weight: 700; color: #01696f; }
    .kpi-sub   { font-size: 0.8rem; color: #7a7974; }
    .section-header {
        font-size: 1.1rem; font-weight: 600; color: #28251d;
        border-left: 3px solid #01696f; padding-left: 0.6rem;
        margin: 1.2rem 0 0.6rem 0;
    }
    div[data-testid="stMetric"] label { font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return get_district_data()

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Emblem_of_Jammu_%26_Kashmir.svg/120px-Emblem_of_Jammu_%26_Kashmir.svg.png", width=80)
    st.markdown("## 🏔️ J&K Census 2011")
    st.markdown("---")

    division_filter = st.multiselect(
        "Filter by Division",
        options=["All", "Kashmir", "Jammu", "Ladakh"],
        default=["All"]
    )

    all_districts = sorted(df["District"].tolist())
    selected_districts = st.multiselect(
        "Select Districts (leave empty = all)",
        options=all_districts,
        default=[]
    )

    metric_choice = st.selectbox(
        "Primary Metric for Map / Bar",
        options=[
            "Total_Population", "Literacy_Rate", "Sex_Ratio",
            "Child_Sex_Ratio", "Worker_Participation_Rate",
            "Urban_Pct", "Population_Density", "Female_Literacy",
            "Gender_Literacy_Gap"
        ],
        format_func=lambda x: x.replace("_", " ")
    )

    st.markdown("---")
    st.markdown("**Data Source**")
    st.markdown("Census of India 2011  \n[censusindia.gov.in](https://censusindia.gov.in)")

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if "All" not in division_filter and division_filter:
    filtered = filtered[filtered["Division"].isin(division_filter)]
if selected_districts:
    filtered = filtered[filtered["District"].isin(selected_districts)]

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🏔️ Jammu & Kashmir — Census 2011 District Dashboard</div>', unsafe_allow_html=True)
st.caption(f"Showing **{len(filtered)}** of 22 districts · Source: Census of India 2011, censusindia.gov.in")

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
total_pop   = filtered["Total_Population"].sum()
avg_lit     = filtered["Literacy_Rate"].mean()
avg_sex     = filtered["Sex_Ratio"].mean()
avg_csr     = filtered["Child_Sex_Ratio"].mean()
urban_pct   = (filtered["Urban_Population"].sum() / filtered["Total_Population"].sum() * 100)
avg_wpr     = filtered["Worker_Participation_Rate"].mean()

k1.metric("👥 Total Population",  f"{total_pop:,.0f}")
k2.metric("📚 Avg Literacy Rate", f"{avg_lit:.1f}%")
k3.metric("⚖️ Avg Sex Ratio",      f"{avg_sex:.0f}")
k4.metric("👶 Child Sex Ratio",    f"{avg_csr:.0f}")
k5.metric("🏙️ Urban Share",        f"{urban_pct:.1f}%")
k6.metric("💼 Worker Part. Rate",  f"{avg_wpr:.1f}%")

st.markdown("---")

# ── Row 1: Bar chart + Urban/Rural Pie ───────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f'<div class="section-header">District-wise {metric_choice.replace("_"," ")}</div>', unsafe_allow_html=True)
    bar_df = filtered.sort_values(metric_choice, ascending=True)
    color_map = {"Kashmir": "#01696f", "Jammu": "#da7101", "Ladakh": "#7a39bb"}
    fig_bar = px.bar(
        bar_df, x=metric_choice, y="District", orientation="h",
        color="Division", color_discrete_map=color_map,
        template="plotly_white",
        labels={metric_choice: metric_choice.replace("_", " "), "District": ""},
        height=520
    )
    fig_bar.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
        margin=dict(l=10, r=20, t=30, b=10), font_family="Inter, sans-serif"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Urban vs Rural Split</div>', unsafe_allow_html=True)
    urban_total = filtered["Urban_Population"].sum()
    rural_total = filtered["Rural_Population"].sum()
    fig_pie = px.pie(
        values=[urban_total, rural_total],
        names=["Urban", "Rural"],
        color_discrete_sequence=["#01696f", "#da7101"],
        template="plotly_white", height=250,
        hole=0.45
    )
    fig_pie.update_traces(textposition="outside", textinfo="percent+label")
    fig_pie.update_layout(margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="section-header">Division Population Share</div>', unsafe_allow_html=True)
    div_df = filtered.groupby("Division")["Total_Population"].sum().reset_index()
    fig_div = px.pie(
        div_df, values="Total_Population", names="Division",
        color="Division", color_discrete_map=color_map,
        template="plotly_white", height=250, hole=0.45
    )
    fig_div.update_traces(textposition="outside", textinfo="percent+label")
    fig_div.update_layout(margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
    st.plotly_chart(fig_div, use_container_width=True)

# ── Row 2: Literacy Comparison + Sex Ratio ────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Male vs Female Literacy Rate (%)</div>', unsafe_allow_html=True)
    lit_df = filtered.sort_values("Literacy_Rate", ascending=False)
    fig_lit = go.Figure()
    fig_lit.add_trace(go.Bar(
        name="Male", x=lit_df["District"], y=lit_df["Male_Literacy"],
        marker_color="#01696f", opacity=0.85
    ))
    fig_lit.add_trace(go.Bar(
        name="Female", x=lit_df["District"], y=lit_df["Female_Literacy"],
        marker_color="#da7101", opacity=0.85
    ))
    fig_lit.update_layout(
        barmode="group", template="plotly_white", height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.01),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_tickangle=-45, font_family="Inter, sans-serif",
        yaxis_title="Literacy Rate (%)"
    )
    st.plotly_chart(fig_lit, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Sex Ratio & Child Sex Ratio</div>', unsafe_allow_html=True)
    sr_df = filtered.sort_values("Sex_Ratio", ascending=False)
    fig_sr = go.Figure()
    fig_sr.add_trace(go.Scatter(
        x=sr_df["District"], y=sr_df["Sex_Ratio"],
        mode="lines+markers", name="Sex Ratio",
        line=dict(color="#01696f", width=2),
        marker=dict(size=8)
    ))
    fig_sr.add_trace(go.Scatter(
        x=sr_df["District"], y=sr_df["Child_Sex_Ratio"],
        mode="lines+markers", name="Child Sex Ratio (0-6)",
        line=dict(color="#a12c7b", width=2, dash="dot"),
        marker=dict(size=8)
    ))
    fig_sr.add_hline(y=1000, line_dash="dash", line_color="gray",
                     annotation_text="National Avg (1000)", annotation_position="top right")
    fig_sr.update_layout(
        template="plotly_white", height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.01),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_tickangle=-45, font_family="Inter, sans-serif",
        yaxis_title="Per 1000 Males"
    )
    st.plotly_chart(fig_sr, use_container_width=True)

# ── Row 3: Scatter + Worker breakdown ────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="section-header">Literacy Rate vs Population Density</div>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered, x="Population_Density", y="Literacy_Rate",
        size="Total_Population", color="Division",
        text="District", color_discrete_map=color_map,
        template="plotly_white", height=350,
        labels={"Population_Density": "Population Density (per sq km)",
                "Literacy_Rate": "Literacy Rate (%)"},
        size_max=50
    )
    fig_scatter.update_traces(textposition="top center", textfont_size=9)
    fig_scatter.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.01),
        font_family="Inter, sans-serif"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col6:
    st.markdown('<div class="section-header">Main vs Marginal Workers</div>', unsafe_allow_html=True)
    wk_df = filtered.sort_values("Total_Workers", ascending=False).head(15)
    fig_wk = go.Figure()
    fig_wk.add_trace(go.Bar(
        name="Main Workers", x=wk_df["District"], y=wk_df["Main_Workers"],
        marker_color="#006494"
    ))
    fig_wk.add_trace(go.Bar(
        name="Marginal Workers", x=wk_df["District"], y=wk_df["Marginal_Workers"],
        marker_color="#d19900"
    ))
    fig_wk.update_layout(
        barmode="stack", template="plotly_white", height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.01),
        font_family="Inter, sans-serif", yaxis_title="Workers"
    )
    st.plotly_chart(fig_wk, use_container_width=True)

# ── Row 4: Treemap ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Population Treemap by Division → District</div>', unsafe_allow_html=True)
fig_tree = px.treemap(
    filtered, path=["Division", "District"],
    values="Total_Population", color="Literacy_Rate",
    color_continuous_scale="Teal",
    template="plotly_white", height=380,
    color_continuous_midpoint=filtered["Literacy_Rate"].mean(),
    labels={"Literacy_Rate": "Literacy Rate (%)"}
)
fig_tree.update_layout(margin=dict(l=10, r=10, t=30, b=10))
st.plotly_chart(fig_tree, use_container_width=True)

# ── Data Table ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 District-wise Data Table</div>', unsafe_allow_html=True)

display_cols = [
    "District", "Division", "Total_Population", "Urban_Pct", "Rural_Pct",
    "Literacy_Rate", "Male_Literacy", "Female_Literacy", "Gender_Literacy_Gap",
    "Sex_Ratio", "Child_Sex_Ratio", "Worker_Participation_Rate",
    "Total_Workers", "Main_Workers", "Marginal_Workers",
    "Population_Density", "Households", "Area_sqkm"
]
st.dataframe(
    filtered[display_cols].sort_values("Total_Population", ascending=False)
    .style.format({
        "Total_Population": "{:,.0f}", "Urban_Pct": "{:.1f}%", "Rural_Pct": "{:.1f}%",
        "Literacy_Rate": "{:.2f}%", "Male_Literacy": "{:.2f}%", "Female_Literacy": "{:.2f}%",
        "Gender_Literacy_Gap": "{:.2f}",
        "Worker_Participation_Rate": "{:.2f}%",
        "Total_Workers": "{:,.0f}", "Main_Workers": "{:,.0f}", "Marginal_Workers": "{:,.0f}",
        "Population_Density": "{:.1f}", "Households": "{:,.0f}", "Area_sqkm": "{:,.0f}"
    }).background_gradient(subset=["Literacy_Rate"], cmap="YlGn")
     .background_gradient(subset=["Total_Population"], cmap="Blues"),
    use_container_width=True, height=420
)

# ── Downloads ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">⬇️ Download Data</div>', unsafe_allow_html=True)
dl1, dl2, dl3 = st.columns(3)

@st.cache_data
def to_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

@st.cache_data
def to_excel(dataframe):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="JK_Census_2011")
        # Summary sheet
        summary = pd.DataFrame({
            "Metric": ["Total Population", "Avg Literacy Rate", "Avg Sex Ratio",
                       "Avg Child Sex Ratio", "Urban Population %", "Total Households"],
            "Value": [
                f"{dataframe['Total_Population'].sum():,.0f}",
                f"{dataframe['Literacy_Rate'].mean():.2f}%",
                f"{dataframe['Sex_Ratio'].mean():.0f}",
                f"{dataframe['Child_Sex_Ratio'].mean():.0f}",
                f"{(dataframe['Urban_Population'].sum()/dataframe['Total_Population'].sum()*100):.2f}%",
                f"{dataframe['Households'].sum():,.0f}"
            ]
        })
        summary.to_excel(writer, index=False, sheet_name="Summary")
    return buf.getvalue()

with dl1:
    st.download_button(
        label="📥 Download CSV (Filtered)",
        data=to_csv(filtered[display_cols]),
        file_name="jk_census_2011_filtered.csv",
        mime="text/csv", use_container_width=True
    )

with dl2:
    st.download_button(
        label="📊 Download Excel (Filtered)",
        data=to_excel(filtered),
        file_name="jk_census_2011_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with dl3:
    st.download_button(
        label="📥 Download Full Dataset (CSV)",
        data=to_csv(df[display_cols]),
        file_name="jk_census_2011_full.csv",
        mime="text/csv", use_container_width=True
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<small>Data Source: Census of India 2011 · censusindia.gov.in · "
    "Primary Census Abstract (PCA) · District Census Handbook (DCHB) · "
    "Built with Streamlit & Plotly</small>",
    unsafe_allow_html=True
)
