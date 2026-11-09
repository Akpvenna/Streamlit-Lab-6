# 🏁 FIA WEC Motorsport Telemetry Dashboard

An interactive, web-based data analytics application built with **Streamlit** to explore, analyze, and visualize official telemetry and race strategy data from the FIA World Endurance Championship (WEC). 

This dashboard is designed to help race engineers and analysts monitor fleet performance, analyze stint efficiency, and investigate vehicle outliers dynamically using real Al Kamel timing data.

## 🚀 Features

- **Interactive Filtering:** Sidebar controls allow users to dynamically filter the telemetry dataset by Vehicle Class (Hypercar, LMP2, LMGT3) and Minimum Laps Completed.
- **Live KPIs:** Real-time metrics tracking the total active cars, average fleet top speed, and total pitstops across the selected grid.
- **Exploratory Data Analysis (EDA):**
  - **Bar Charts:** Visualizes maximum top speeds by individual car.
  - **Line Charts:** Tracks the average lap speed (KPH) across different vehicles.
  - **Scatter Plots:** Maps the correlation between Laps Completed and Top Speed to evaluate endurance performance and reliability.
- **Analytical Insights:** Automatically generated strategic observations regarding class stratification, pitstop penalties, and overall pace consistency.

## 🛠️ Technologies Used

- **Python 3.x**
- **Streamlit** (Web framework and UI layout)
- **Pandas** (Data manipulation and aggregation)
- **Matplotlib** (Data visualization)

## 📂 Dataset Requirement

This application requires an official Al Kamel timing dataset to function correctly. 
- **Expected File:** `23_Analysis_Race_Hour 24.CSV`
- The file must be placed in the root directory alongside the Python script. The script aggregates raw lap-by-lap data into summarized car profiles automatically.

## ⚙️ Installation & Setup

1. **Clone or Download the Repository:**
   Ensure both the Python script and the CSV dataset are in the same folder.

2. **Install Required Dependencies:**
   Open your terminal/command prompt and install the necessary Python libraries:
   
```bash
   pip install streamlit pandas matplotlib
