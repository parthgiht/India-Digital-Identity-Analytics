# 📊 Aadhaar Enrollment Analytics Dashboard
**A comprehensive, interactive analytics platform for visualizing and analyzing Aadhaar enrollment data across India**


![image_alt](https://github.com/parthgiht/India-Digital-Identity-Analytics/blob/main/Aadhaar.jpeg?raw=true)


---

## 📑 Table of Contents

- Overview
- Key Features
- Technology Stack
- Screenshots
- Usage
- Project Structure
- Data Requirements
- Features in Detail
- Acknowledgments

---

## 🎯 Overview

The **Aadhaar Enrollment Analytics Dashboard** is a powerful data visualization and analysis platform designed to provide comprehensive insights into India's Aadhaar enrollment ecosystem. Built with modern Python frameworks, this dashboard offers real-time data exploration, geographic visualization, and statistical analysis across multiple dimensions.

### Why This Dashboard?

- 🔍 **Deep Insights**: Analyze enrollment patterns across 36+ states and 700+ districts
- 🗺️ **Geographic Intelligence**: Interactive maps for state and district-level analysis
- 📈 **Temporal Analysis**: Track trends across years, quarters, months, and days
- 👥 **Demographic Breakdown**: Understand age group distributions and enrollment patterns
- 🎛️ **Advanced Filtering**: Multi-dimensional filtering for precise data exploration
- 📊 **Export Ready**: Download filtered datasets for further analysis

---

## ✨ Key Features

### 🗺️ **Interactive Geographic Visualizations**
- **India Choropleth Map**: Color-coded state-wise enrollment visualization
- **District-level Analysis**: Treemap and Sunburst charts for district comparison
- **Hover Interactions**: Detailed tooltips with enrollment statistics
- **Zoom & Pan Controls**: Explore regions in detail

### 📅 **Comprehensive Temporal Analysis**
- **Monthly Trends**: Dual-axis charts showing total and average enrollments
- **Quarterly Distribution**: Bar charts and pie charts for seasonal patterns
- **Day-of-Week Analysis**: Identify peak enrollment days
- **Weekend vs Weekday**: Compare enrollment patterns by day type
- **Year-over-Year Growth**: Track enrollment growth rates

### 👥 **Demographic Insights**
- **Age Group Distribution**: 0-5 years, 5-17 years, 18+ years breakdown
- **Minor vs Adult Analysis**: Comprehensive underage enrollment tracking
- **Interactive Pie & Bar Charts**: Multiple visualization options

### 🎛️ **Advanced Filtering System**
- **State Selection**: Single or multiple state filtering
- **Year Selection**: Multi-year comparison capability
- **Quarter Selection**: Seasonal analysis options
- **Day Type Filtering**: Weekday/Weekend segregation
- **Real-time Updates**: Instant dashboard refresh on filter changes

### 📊 **Statistical Analysis**
- **Distribution Analysis**: Histograms for any numerical metric
- **Descriptive Statistics**: Mean, median, std deviation, min/max values
- **Comparative Analysis**: Side-by-side state comparisons
- **Data Explorer**: Raw data viewing with column selection

### 💾 **Data Export**
- **CSV Download**: Export filtered datasets
- **Custom Column Selection**: Choose specific fields to export
- **Preserves Filters**: Exported data respects all active filters

---

## 📸 Screenshots

### Dashboard Overview
![image_alt](https://via.placeholder.com/800x400?text=Dashboard+Main+View)

### Interactive India Map
![image_alt](https://via.placeholder.com/800x400?text=Interactive+India+Map)

### District Analysis
![image_alt](https://via.placeholder.com/800x400?text=District+Level+Analysis)

### Temporal Trends
![image_alt](https://via.placeholder.com/800x400?text=Temporal+Trends)

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.8+ |
| **Web Framework** | Streamlit 1.31.0 |
| **Data Processing** | Pandas 2.1.4, NumPy 1.26.3 |
| **Visualization** | Plotly 5.18.0 |
| **Maps** | Plotly Choropleth, Treemap, Sunburst |
| **Styling** | Custom CSS, HTML |

---

## 💡 Usage

### Basic Usage

**1. Launch the Dashboard**
```bash
streamlit run app.py
```

**2. Apply Filters (Sidebar)**
- Select states, years, quarters
- Choose day type (All/Weekday/Weekend)
- Filters apply across all visualizations

**3. Explore Visualizations**
- Navigate through different tabs
- Hover over charts for detailed information
- Click on interactive elements for drill-down

**4. Export Data**
- Select desired columns in Data Explorer
- Click "Download Filtered Data as CSV"


---

## 📁 Project Structure
```
aadhaar-enrollment-analytics/
│
├── app.py                                      # Main Streamlit application
├── Aadhaar_enrollment_FeatureEngineering.csv  # Dataset (not included in repo)
├── requirements.txt                            # Python dependencies
├── README.md                                   # Project documentation
├── .gitignore                                  # Git ignore rules
│
├── assets/                                     # (Optional) Images and resources
│   ├── screenshots/
│   └── aadhaar_logo.png
│
└── docs/                                       # (Optional) Additional documentation
    ├── DATA_DICTIONARY.md
    └── USER_GUIDE.md
```

---

## 📊 Data Requirements

### Expected Dataset Format

The dashboard expects a CSV file with the following structure:

| Column Name | Type | Description |
|------------|------|-------------|
| `state` | String | State name |
| `district` | String | District name |
| `year` | Integer | Enrollment year |
| `quarter` | Integer | Quarter (1-4) |
| `month` | Integer | Month (1-12) |
| `day_of_week` | Integer | Day (0=Monday, 6=Sunday) |
| `is_weekend` | Integer | Weekend flag (0/1) |
| `total_enrollment` | Integer | Total enrollments |
| `age_0_5` | Integer | Age group 0-5 years |
| `age_5_17` | Integer | Age group 5-17 years |
| `age_18_greater` | Integer | Age group 18+ years |
| `minor_count` | Integer | Total minors (0-17) |

---

## 🔧 Features in Detail

### 1. Key Performance Indicators (KPIs)

Five main KPIs displayed at the top:
- **Total Enrollments**: Aggregate across filtered data
- **Average Enrollment**: Mean enrollment per record
- **Total States**: Number of unique states
- **Total Districts**: Number of unique districts
- **Total Records**: Count of data points

### 2. Temporal Analysis Module

**Monthly Trends**
- Dual-axis chart: Total (bar) + Average (line)
- Identifies peak enrollment months
- Data table with complete statistics

**Quarterly Analysis**
- Bar chart for total enrollments
- Pie chart for distribution
- Seasonal pattern identification

**Day of Week Patterns**
- Average enrollment by day
- Weekend vs Weekday comparison
- Identifies operational patterns

### 3. Geographic Analysis Module

**Interactive India Map**
- Choropleth visualization
- Color-coded by enrollment volume
- Hover for state statistics
- Identifies high/low performing regions

**District Drill-Down**
- Select any state
- Treemap: Top 30 districts
- Sunburst: Top 20 districts (hierarchical)
- Bar chart: Top 20 ranked
- Complete district table

### 4. Demographic Analysis Module

**Age Group Distribution**
- Three categories: 0-5, 5-17, 18+
- Pie chart (proportional)
- Bar chart (absolute numbers)
- Individual metrics for each group

**Minor vs Adult Analysis**
- Binary classification
- Donut chart visualization
- Percentage calculations
- Policy-relevant insights

### 5. Comparative Analysis Module

**State Comparison**
- Multi-state selection (up to 5)
- Line chart: Monthly trends
- Statistics table: Mean, median, std dev
- Side-by-side analysis

**Year-over-Year**
- Growth rate calculations
- Bar chart: Total by year
- Line chart: Growth percentage
- Trend identification

### 6. Data Explorer

**Interactive Table**
- Column selection
- First 100 records displayed
- Full dataset available
- Sort and filter capabilities

**Export Functionality**
- CSV download
- Respects active filters
- Custom column selection
- One-click export

### 7. Statistical Summary

**Distribution Analysis**
- Histogram for any metric
- Bin customization
- Color-coded visualization

**Descriptive Statistics**
- Mean, Median, Std Dev
- Min, Max values
- Metric selection dropdown

---

## 🙏 Acknowledgments

- **Streamlit Team** - For the amazing web framework
- **Plotly** - For powerful interactive visualizations
- **UIDAI** - For Aadhaar enrollment data initiatives
- **Python Community** - For excellent libraries and support
- **Open Source Contributors** - For inspiring this project

---

<div align="center">

**Made with ❤️ by Parth Patel**

**Data Analyst | Visualization Specialist | Business Intelligence Expert**

© 2025 All Rights Reserved

</div>
