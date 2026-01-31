import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="US Accident Analytics",
    layout="wide"
)

st.title("🚗 Phân tích Tai nạn Giao thông (Big Data)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_parquet("dtb_data.parquet")

    # Convert datetime
    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")
    df["Year"] = df["Start_Time"].dt.year

    return df

df = load_data()

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric(
    "Tổng số tai nạn",
    f"{len(df):,}"
)

col2.metric(
    "Khoảng cách TB (mile)",
    round(df["Distance(mi)"].mean(), 3)
)

col3.metric(
    "Khoảng cách max (mile)",
    round(df["Distance(mi)"].max(), 3)
)

# =========================
# SEVERITY
# =========================
st.subheader("⚠️ Severity")

severity_df = (
    df.groupby("Severity")
      .size()
      .reset_index(name="Count")
      .set_index("Severity")
)

st.bar_chart(severity_df)

# =========================
# ACCIDENTS BY YEAR
# =========================
st.subheader("📅 Tai nạn theo năm")

year_df = (
    df.groupby("Year")
      .size()
      .reset_index(name="Count")
      .sort_values("Year")
      .set_index("Year")
)

st.line_chart(year_df)

# =========================
# DAY / NIGHT
# =========================
st.subheader("🌞 Ngày / 🌙 Đêm")

sun_df = (
    df.groupby("Sunrise_Sunset")
      .size()
      .reset_index(name="Count")
      .set_index("Sunrise_Sunset")
)

st.bar_chart(sun_df)
