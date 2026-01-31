import streamlit as st
import vaex

st.set_page_config(page_title="US Accident Analytics", layout="wide")
st.title("🚗 Phân tích Tai nạn Giao thông (Big Data)")

@st.cache_data
def load_data():
    df = vaex.open("dtb_data.parquet")
    df['Start_Time'] = df['Start_Time'].astype('datetime64')
    df['Year'] = df['Start_Time'].dt.year
    return df

df = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Tổng số tai nạn", f"{df.count():,}")
col2.metric("Khoảng cách TB (mile)", round(df.mean(df["Distance(mi)"]), 3))
col3.metric("Khoảng cách max (mile)", round(df.max(df["Distance(mi)"]), 3))

st.subheader("⚠️ Severity")
st.bar_chart(
    df.groupby("Severity", agg=vaex.agg.count())
      .to_pandas_df()
      .set_index("Severity")
)

st.subheader("📅 Tai nạn theo năm")
st.line_chart(
    df.groupby("Year", agg=vaex.agg.count())
      .sort("Year")
      .to_pandas_df()
      .set_index("Year")
)

st.subheader("🌞 Ngày / 🌙 Đêm")
st.bar_chart(
    df.groupby("Sunrise_Sunset", agg=vaex.agg.count())
      .to_pandas_df()
      .set_index("Sunrise_Sunset")
)
