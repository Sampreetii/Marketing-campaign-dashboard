import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Marketing Campaign Dashboard", layout="wide")

st.title("📊 Marketing Campaign Analysis Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your marketing campaign CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Preprocessing ---
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar Filters
    with st.sidebar:
        st.header("🔍 Filters")

        campaign_types = st.multiselect(
            "Select Campaign Types:",
            options=df['Campaign_Type'].unique(),
            default=df['Campaign_Type'].unique()
        )

        channels = st.multiselect(
            "Select Channels Used:",
            options=df['Channel_Used'].unique(),
            default=df['Channel_Used'].unique()
        )

        segments = st.multiselect(
            "Select Customer Segments:",
            options=df['Customer_Segment'].unique(),
            default=df['Customer_Segment'].unique()
        )

        date_range = st.date_input(
            "Select Date Range:",
            [df['Date'].min(), df['Date'].max()]
        )

    # Apply filters
    filtered_df = df[
        (df['Campaign_Type'].isin(campaign_types)) &
        (df['Channel_Used'].isin(channels)) &
        (df['Customer_Segment'].isin(segments)) &
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1]))
    ]

    # --- KPI Boxes ---
    st.markdown("### 📌 Key Performance Indicators")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Avg Conversion Rate", f"{filtered_df['Conversion_Rate'].mean():.2%}")
    kpi2.metric("Avg ROI", f"{filtered_df['ROI'].mean():.2f}")
    kpi3.metric("Total Campaigns", len(filtered_df))

    st.divider()

    # --- Charts ---
    st.markdown("### 📈 Conversion Rate by Channel")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=filtered_df, x="Channel_Used", y="Conversion_Rate", ax=ax1)
    ax1.set_title("Avg Conversion Rate by Channel")
    st.pyplot(fig1)

    st.markdown("### 💡 ROI by Campaign Type")
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=filtered_df, x="Campaign_Type", y="ROI", ax=ax2)
    ax2.set_title("ROI Distribution by Campaign Type")
    st.pyplot(fig2)

    st.markdown("### 📆 Campaign Trend Over Time")
    trend_df = filtered_df.groupby(filtered_df['Date'].dt.to_period("M")).size()
    fig3, ax3 = plt.subplots()
    trend_df.plot(kind='line', marker='o', ax=ax3)
    ax3.set_title("Campaigns Over Time")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Campaign Count")
    st.pyplot(fig3)

else:
    st.info("👆 Upload a CSV file to begin.")
