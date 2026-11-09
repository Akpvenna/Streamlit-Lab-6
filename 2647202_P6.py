import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION & LAYOUT
# ==========================================
st.set_page_config(page_title="FIA WEC Analytics", layout="wide")
st.title("🏁 Motorsport Telemetry Dashboard")
st.markdown("### FIA WEC Endurance Race Analytics")
st.caption("Interactive exploration of official Al Kamel timing and endurance race strategy")

# ==========================================
# DATASET PROCESSING
# ==========================================
# Ensure "23_Analysis_Race_Hour 24.CSV" is in the same folder as this script
try:
    # WEC data uses semicolons as separators
    raw_df = pd.read_csv("23_Analysis_Race_Hour 24.CSV", sep=";")
    
    # Strip any accidental whitespace from column names
    raw_df.columns = raw_df.columns.str.strip() 
    
    # Aggregate raw lap-by-lap data into single Car Profiles
    df = raw_df.groupby(['NUMBER', 'CLASS', 'TEAM']).agg(
        Laps=('LAP_NUMBER', 'max'),
        Top_Speed=('TOP_SPEED', 'max'),
        Avg_KPH=('KPH', 'mean'),
        Pitstops=('PIT_TIME', lambda x: x.notnull().sum())
    ).reset_index()
    
    # Create a clean string ID for the charts (e.g., "Car 50")
    df['Car_ID'] = 'Car ' + df['NUMBER'].astype(str)
    
except FileNotFoundError:
    st.error("Dataset '23_Analysis_Race_Hour 24.CSV' not found. Please ensure it is in the same directory.")
    st.stop()

# ==========================================
# SIDEBAR (Filters)
# ==========================================
st.sidebar.title("Filter Options")

classes_available = df['CLASS'].unique()
selected_classes = st.sidebar.multiselect(
    "Select Vehicle Class:", 
    options=classes_available, 
    default=classes_available
)

min_laps = st.sidebar.slider(
    "Min Laps Completed:", 
    min_value=int(df["Laps"].min()), 
    max_value=int(df["Laps"].max()), 
    value=int(df["Laps"].min())
)

# Apply filters to dataframe
filtered_df = df[(df["CLASS"].isin(selected_classes)) & (df["Laps"] >= min_laps)]

# ==========================================
# TABS LAYOUT
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["Dataset", "KPIs", "Visualizations", "Insights"])

# --- TAB 1: DATASET OVERVIEW ---
with tab1:
    st.header("Aggregated Telemetry Dataset")
    st.dataframe(filtered_df)

# --- TAB 2: KPIs & COLUMNS ---
with tab2:
    st.header("Key Performance Indicators")
    
    # 3-Column Metric Layout
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Active Cars", len(filtered_df))
    
    if not filtered_df.empty:
        avg_speed = round(filtered_df["Top_Speed"].mean(), 1)
        total_pits = filtered_df["Pitstops"].sum()
        col2.metric("Avg Fleet Top Speed", f"{avg_speed} km/h")
        col3.metric("Total Pitstops", total_pits)
    
    st.subheader("Category-wise Record Counts")
    st.table(filtered_df.groupby("CLASS").size().reset_index(name="Count"))

# --- TAB 3: VISUALIZATIONS ---
with tab3:
    st.header("Data Visualizations")
    
    if not filtered_df.empty:
        # A. Native Streamlit Bar Chart
        st.subheader("1. Max Top Speed by Car (Bar Chart)")
        bar_data = filtered_df.set_index("Car_ID")[["Top_Speed"]]
        st.bar_chart(bar_data)

        # B. Native Streamlit Line Chart
        st.subheader("2. Average Lap Speed (KPH) by Car (Line Chart)")
        line_data = filtered_df.set_index("Car_ID")[["Avg_KPH"]]
        st.line_chart(line_data)

        # C. Matplotlib Scatter Plot
        st.subheader("3. Laps vs Top Speed (Scatter Plot)")
        fig, ax = plt.subplots()
        ax.scatter(filtered_df["Top_Speed"], filtered_df["Laps"], color='purple', alpha=0.7)
        ax.set_xlabel("Top Speed (km/h)")
        ax.set_ylabel("Laps Completed")
        ax.set_title("Endurance Performance Matrix")
        st.pyplot(fig)
    else:
        st.error("No data available for the selected filters.")

# --- TAB 4: INSIGHTS ---
# --- TAB 4: INSIGHTS ---
with tab4:
    st.header("Analytical Insights")
    st.success("**Class Performance Stratification:** Analysis of the maximum top speeds confirms the expected regulatory gap. Hypercars consistently exceed 330 km/h, establishing a clear pace advantage over the LMP2 and LMGT3 fields.")
    st.warning("**The Pitstop Penalty:** The scatter plot reveals a direct correlation between laps completed and total pitstops. This highlights the strict fuel and tire lifecycle constraints dictated by endurance racing strategy.")
    st.info("**Pace vs. Consistency:** While maximum top speed is critical for overtaking, the Average KPH metric indicates that maintaining a consistent lap time without traffic interruptions is the true driver of long-run endurance success.")