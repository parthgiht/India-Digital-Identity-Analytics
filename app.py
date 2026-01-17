import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title = "Aadhaar Enrollment Analytics",
    page_icon = "📊",
    layout = "wide",
    initial_sidebar_state = "expanded"
)


st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        font-weight: 700;
    }
    h2 {
        color: #2c3e50;
        font-weight: 600;
    }
    h3 {
        color: #34495e;
        font-weight: 500;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)



#------------ Load data -----------
@st.cache_data
def load_data():
    """Load the featured dataset"""
    try:
        data = pd.read_csv("Aadhaar_enrollment_FeatureEngineering.csv")
        return data
    except FileNotFoundError:
        st.error("Data file not found!")
        st.stop()

data = load_data()



# ------------ Sidebar - Filter --------------
st.sidebar.title("🔍Filter & Options")
st.sidebar.markdown("---")

# State filter 
states = ['All'] + sorted(data['state'].unique().tolist())
selected_states = st.sidebar.multiselect(
    "Select States",
    options = states,
    default = ['All']
)

# Year filter 
years = ['All'] + sorted(data['year'].unique().tolist())
selected_years = st.sidebar.multiselect(
    "Select Years",
    options = years,
    default = ['All']
)

# Quarter filter 
quarters = ['All'] + sorted(data['quarter'].unique().tolist())
selected_quarters = st.sidebar.multiselect(
    "Select Quarter",
    options = quarters,
    default = ['All']
)

# Weekend filter 
weekend_options = st.sidebar.radio(
    "Day Type",
    options = ['All', 'Weekday Only', 'Weekend Only']
)
st.sidebar.markdown("---")
st.sidebar.info("Use filters to explore specific segments of data")



# ------------ Apply Filter ---------------
filtered_data = data.copy()

# State filter 
if 'All' not in selected_states and len(selected_states) > 0:
    filtered_data = filtered_data[filtered_data['state'].isin(selected_states)]

# Year filter 
if 'All' not in selected_years and len(selected_years) > 0:
    filtered_data = filtered_data[filtered_data['year'].isin(selected_years)]

# Quarter filter
if 'All' not in selected_quarters and len(selected_quarters) > 0:
    filtered_data = filtered_data[filtered_data['quarter'].isin(selected_quarters)]

# Weekend filter 
if weekend_options == 'Weekday Only':
    filtered_data = filtered_data[filtered_data['is_weekend'] == 0]
elif weekend_options == 'Weekend Only':
    filtered_data = filtered_data[filtered_data['is_weekend'] == 1]



# ------------ Main Dashboard ----------

# Title and Description

col_img, col_title = st.columns([1, 4])

with col_img:
    st.image("https://i.pinimg.com/1200x/a0/8e/e6/a08ee6eaceb1d5fbb717e81cf16ce9fb.jpg")


with col_title:
    st.title("📊 Aadhaar Enrollment Analytics Dashboard")
    st.markdown("**Comprehensive analysis of aadhaar enrollment data across india**")
st.markdown("---")


# Display filter status 
if len(filtered_data) < len(data):
    st.info(f"🔍 Showing **{len(filtered_data):,}** records out of **{len(data):,}** total records (filtered)")
else:
    st.success(f"📈 Showing all **{len(data):,}** records")
st.markdown("---")



# ------------ Key Performance Indicators (KPIs) -------------
st.header("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_enrollment = filtered_data['total_enrollment'].sum()
    st.metric(
        label = "Total Enrollments",
        value = f"{total_enrollment:,}",
        delta = None 
    )

with col2:
    avg_enrollment = filtered_data['total_enrollment'].mean()
    st.metric(
        label = "Average Enrollment",
        value = f"{avg_enrollment:,.0f}",
        delta = None 
    )

with col3:
    total_states = filtered_data['state'].nunique()
    st.metric(
        label = "Total States",
        value = f"{total_states}",
        delta = None
    )

with col4:
    total_districts = filtered_data['district'].nunique()
    st.metric(
        label = "Total Districts",
        value = f"{total_districts}",
        delta = None 
    )

with col5:
    total_records = len(filtered_data)
    st.metric(
        label = "Total Records",
        value = f"{total_records:,}",
        delta = None 
    )

st.markdown("---")





# ------------- Time Series Analysis --------------
st.header("📅 Temporal Analysis")

tab1, tab2, tab3 = st.tabs(["Monthly Trends", "Quarterly Analysis", "Day of Week"])

with tab1:
    st.subheader("Monthly Enrollment Trends")

    # Group by month 
    monthly_data = filtered_data.groupby('month')['total_enrollment'].agg(['sum', 'mean','count']).reset_index()
    monthly_data.columns = ['Month', 'Total_Enrollment', 'Avg_Enrollment', 'Records']

    # Create figure with secondary y-axis
    fig = make_subplots(specs = [[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x = monthly_data['Month'], y = monthly_data['Total_Enrollment'],
               name = 'Total Enrollment', marker_color = 'steelblue'),
               secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x = monthly_data['Month'], y = monthly_data['Avg_Enrollment'],
                   name = 'Average Enrollment', mode = 'lines+markers',
                   marker = dict(size = 8, color = 'orange'), 
                   line = dict(width = 3)),
                   secondary_y = True,
    )


    fig.update_layout(
        title_text = "Monthly Enrollment Analysis",
        hovermode = 'x unified',
        autosize = True,
        height = 500,
        margin = dict(l = 80, r = 40, t = 80, b = 60)
    )

    fig.update_xaxes(title_text = "Month")
    fig.update_yaxes(title_text = "Total Enrollment", secondary_y = False)
    fig.update_yaxes(title_text = "Average Enrollment", secondary_y = True)

    st.plotly_chart(fig, use_container_width = True)

    st.dataframe(monthly_data, use_container_width = True)


with tab2:
    st.subheader("Quarterly Enrollment Distribution")
    
    quarterly_data = filtered_data.groupby('quarter')['total_enrollment'].agg(['sum', 'mean']).reset_index()
    quarterly_data.columns = ['Quarter', 'Total_Enrollment', 'Avg_Enrollment']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig = px.bar(quarterly_data, x='Quarter', y='Total_Enrollment',
                     title='Total Enrollment by Quarter',
                     color='Total_Enrollment',
                     color_continuous_scale='Blues')
        fig.update_layout(
            autosize = True,
            height=450,
            margin = dict(l = 60, r = 40, t = 80, b = 60))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart
        fig = px.pie(quarterly_data, values='Total_Enrollment', names='Quarter',
                     title='Enrollment Distribution by Quarter',
                     hole=0.4)
        fig.update_layout(
            autosize=True,
            margin=dict(l=60, r=40, t=80, b=60),
            height=450)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Day of Week Patterns")
    
    dow_data = filtered_data.groupby('day_of_week')['total_enrollment'].agg(['sum', 'mean']).reset_index()
    dow_data.columns = ['Day_of_Week', 'Total_Enrollment', 'Avg_Enrollment']
    dow_data['Day_Name'] = dow_data['Day_of_Week'].map({
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    })
    
    fig = px.bar(dow_data, x='Day_Name', y='Avg_Enrollment',
                 title='Average Enrollment by Day of Week',
                 color='Avg_Enrollment',
                 color_continuous_scale='Viridis')
    fig.update_layout(autosize=True,
                      height=450,
                      margin=dict(l=60, r=40, t=80, b=60))
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekend vs Weekday comparison
    weekend_comparison = filtered_data.groupby('is_weekend')['total_enrollment'].agg(['sum', 'mean']).reset_index()
    weekend_comparison['Type'] = weekend_comparison['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
    
    col1, col2 = st.columns(2)
    
    weekday_df = weekend_comparison.loc[
    weekend_comparison['Type'] == 'Weekday'
]

with col1:
    if weekday_df.shape[0] > 0:
        st.metric(
            "Weekday Avg Enrollment",
            f"{weekday_df['mean'].iloc[0]:,.0f}"
        )
    else:
        st.metric("Weekday Avg Enrollment", "N/A")

    weekend_df = weekend_comparison.loc[
    weekend_comparison['Type'] == 'Weekend'
]

with col2:
    if weekend_df.shape[0] > 0:
        st.metric(
            "Weekend Avg Enrollment",
            f"{weekend_df['mean'].iloc[0]:,.0f}"
        )
    else:
        st.metric("Weekend Avg Enrollment", "N/A")

st.markdown("---")







# ------------- Geographical Analysis -----------
st.header("🗺️ Geographic Analysis")

tab1, tab2, tab3 = st.tabs(["Interactive India Map", "State-wise Analysis", "District-wise Analysis"])

with tab1:
    st.subheader("📍 Interactive Map - State-wise Enrollment")
    
    # Prepare data for map
    state_map_data = filtered_data.groupby('state')['total_enrollment'].agg(['sum', 'mean', 'count']).reset_index()
    state_map_data.columns = ['state', 'Total_Enrollment', 'Avg_Enrollment', 'Records']
    
    # Create choropleth map
    fig = px.choropleth(
        state_map_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='Total_Enrollment',
        color_continuous_scale='Viridis',
        hover_name='state',
        hover_data={
            'state': False,
            'Total_Enrollment': ':,',
            'Avg_Enrollment': ':,.0f',
            'Records': ':,'
        },
        title='Total Enrollment by State - Interactive Map',
        labels={'Total_Enrollment': 'Total Enrollments'}
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )
    
    fig.update_layout(
        autosize=True,
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Map insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_state = state_map_data.nlargest(1, 'Total_Enrollment').iloc[0]
        st.metric(
            "🏆 Highest Enrollment State",
            top_state['state'],
            f"{top_state['Total_Enrollment']:,}"
        )
    
    with col2:
        bottom_state = state_map_data.nsmallest(1, 'Total_Enrollment').iloc[0]
        st.metric(
            "📉 Lowest Enrollment State",
            bottom_state['state'],
            f"{bottom_state['Total_Enrollment']:,}"
        )
    
    with col3:
        avg_state_enrollment = state_map_data['Total_Enrollment'].mean()
        st.metric(
            "📊 Average per State",
            f"{avg_state_enrollment:,.0f}"
        )
    
    st.markdown("---")
    
    # State selection for detailed view
    st.subheader("🔍 District-wise Map View")
    
    selected_map_state = st.selectbox(
        "Select a state to view district-level enrollment",
        options=sorted(filtered_data['state'].unique())
    )
    
    if selected_map_state:
        # Filter data for selected state
        state_district_data = filtered_data[filtered_data['state'] == selected_map_state]
        district_summary = state_district_data.groupby('district')['total_enrollment'].agg(['sum', 'mean', 'count']).reset_index()
        district_summary.columns = ['District', 'Total_Enrollment', 'Avg_Enrollment', 'Records']
        district_summary = district_summary.sort_values('Total_Enrollment', ascending=False)

        # Create two columns for different visualizations
        col_vis1, col_vis2 = st.columns(2)
        
        with col_vis1:
            # Treemap visualization
            st.markdown(f"#### 📦 Treemap - District Enrollment in {selected_map_state}")
            fig_tree = px.treemap(
                district_summary.head(30),
                path=['District'],
                values='Total_Enrollment',
                color='Total_Enrollment',
                color_continuous_scale='Viridis',
                hover_data={'Total_Enrollment': ':,', 'Avg_Enrollment': ':,.0f'},
                title=f'Top 30 Districts Treemap'
            )
            fig_tree.update_layout(
                height=500,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            fig_tree.update_traces(
                textposition='middle center',
                textfont_size=11
            )
            st.plotly_chart(fig_tree, use_container_width=True)
        
        with col_vis2:
            # Sunburst chart
            st.markdown(f"#### ☀️ Sunburst - District Distribution")
            # Add state column for sunburst
            district_sunburst = district_summary.head(20).copy()
            district_sunburst['state'] = selected_map_state
            
            fig_sun = px.sunburst(
                district_sunburst,
                path=['state', 'District'],
                values='Total_Enrollment',
                color='Total_Enrollment',
                color_continuous_scale='Plasma',
                hover_data={'Total_Enrollment': ':,'},
                title=f'Top 20 Districts Hierarchy'
            )
            fig_sun.update_layout(
                height=500,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_sun, use_container_width=True)
        
        st.info("💡 **Visualization Info**: Treemap and Sunburst sizes represent enrollment volume. Larger boxes/segments = higher enrollments.")
        
        st.markdown("---")


        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Horizontal bar chart for districts
            fig = px.bar(
                district_summary.head(20),
                x='Total_Enrollment',
                y='District',
                orientation='h',
                title=f'Top 20 Districts in {selected_map_state}',
                color='Total_Enrollment',
                color_continuous_scale='Teal',
                hover_data={'Total_Enrollment': ':,', 'Avg_Enrollment': ':,.0f'}
            )
            fig.update_layout(
                autosize=True,
                height=600,
                margin=dict(l=150, r=40, t=80, b=60),
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"#### {selected_map_state} Summary")
            st.metric("Total Districts", len(district_summary))
            st.metric("Total Enrollments", f"{district_summary['Total_Enrollment'].sum():,}")
            st.metric("Average per District", f"{district_summary['Avg_Enrollment'].mean():,.0f}")
            
            st.markdown("---")
            st.markdown("#### Top 5 Districts")
            for idx, row in district_summary.head(5).iterrows():
                st.write(f"**{row['District']}**")
                st.caption(f"{row['Total_Enrollment']:,} enrollments")
        
        # Detailed district table
        st.markdown(f"#### All Districts in {selected_map_state}")
        st.dataframe(district_summary, use_container_width=True)

with tab2:
    st.subheader("State-wise Enrollment Statistics")
    
    state_data = filtered_data.groupby('state')['total_enrollment'].agg(['sum', 'mean', 'count']).reset_index()
    state_data.columns = ['State', 'Total_Enrollment', 'Avg_Enrollment', 'Records']
    state_data = state_data.sort_values('Total_Enrollment', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Top 15 states bar chart
        top_states = state_data.head(15)
        fig = px.bar(top_states,
                     x='Total_Enrollment',
                     y='State',
                     title='Top 15 States by Total Enrollment',
                     orientation='h',
                     color='Total_Enrollment',
                     color_continuous_scale='Blues')
        fig.update_layout(autosize=True, height=550, margin=dict(l=180, r=40, t=80, b=60))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Summary Statistics")
        st.metric('Total States', len(state_data))
        st.metric("Highest Enrollment", f"{state_data['Total_Enrollment'].max():,}")
        st.metric("Top State", state_data.iloc[0]['State'])
        
        st.markdown("---")
        st.markdown("#### Top 5 States")
        for idx, row in state_data.head(5).iterrows():
            st.write(f"**{row['State']}**: {row['Total_Enrollment']:,}")
    
    st.markdown("#### Complete State-wise Data")
    st.dataframe(state_data, use_container_width=True)

with tab3:
    st.subheader("District-wise Enrollment Analysis")
    
    district_data = filtered_data.groupby(['state', 'district'])['total_enrollment'].agg(['sum', 'mean', 'count']).reset_index()
    district_data.columns = ['State', 'District', 'Total_Enrollment', 'Avg_Enrollment', 'Records']
    district_data = district_data.sort_values('Total_Enrollment', ascending=False)
    
    # Top 20 districts
    top_districts = district_data.head(20)
    top_districts['State_District'] = top_districts['State'].fillna('').astype(str) + ' - ' + top_districts['District'].fillna('').astype(str)
    
    fig = px.bar(top_districts,
                 x='Total_Enrollment',
                 y='State_District',
                 title='Top 20 Districts by Total Enrollment',
                 orientation='h',
                 color='Total_Enrollment',
                 color_continuous_scale='Greens')
    fig.update_layout(autosize=True, height=700, margin=dict(l=250, r=40, t=90, b=60))
    st.plotly_chart(fig, use_container_width=True)
    
    # District statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Districts", len(district_data))
    
    with col2:
        st.metric("Top District", f"{district_data.iloc[0]['District']}")
    
    with col3:
        st.metric("Highest Enrollment", f"{district_data['Total_Enrollment'].max():,}")
    
    # Full district table
    st.markdown("#### Complete District-wise Data")
    st.dataframe(district_data, use_container_width=True)

st.markdown("---")




#-------------- Demographic Analysis ------------
st.header("👥 Demographic Analysis")

# Calculate age group totals
if 'age_0_5' in filtered_data.columns:
    age_0_5_total = filtered_data['age_0_5'].sum()
    age_5_17_total = filtered_data['age_5_17'].sum()
    age_18_total = filtered_data['age_18_greater'].sum()

    age_distribution = pd.DataFrame({
        'Age_Group': ['0-5 years', '5-17 years', '18+ years'],
        'Count': [age_0_5_total, age_5_17_total, age_18_total]
    })

    col1, col2 = st.columns(2)


    with col1:
        # Pie chart 
        fig = px.pie(age_distribution, values = 'Count', names = 'Age_Group', 
                     title = 'Age Group Distribution',
                     hole = 0.4,
                     color_discrete_sequence = px.colors.sequential.RdBu)
        fig.update_layout(autosize=True,
                          height=450,
                          margin=dict(l=60, r=40, t=80, b=60))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bar chart 
        fig = px.bar(age_distribution, x = 'Age_Group', y = 'Count', 
                     title = 'Enrollment Count by Age Group',
                     color = 'Age_Group',
                     color_discrete_sequence = ['#3498db', '#2ecc71', '#e74c3c'])
        fig.update_layout(autosize=True,
                          height=450,
                          margin=dict(l=60, r=40, t=80, b=60),
                          showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Age 0-5", f"{age_0_5_total:,}")

    with col2:
        st.metric("Age 5-17", f"{age_5_17_total:,}")

    with col3:
        st.metric("Age 18+", f"{age_18_total:,}")


    
    # Minor vs Adult analysis 
    if 'minor_dount' in filtered_data.columns:
        st.markdown("---")
        st.subheader("Minor vs Adult Enrollment")

        total_minors = filtered_data['minor_count'].sum()
        total_adults = age_18_total 

        minor_adult_data = pd.DataFrame({
            'Category': ['Minors (0-17)', 'Adults (18+)'],
            'Count': [total_minors, total_adults]
        })


        ocl1, col2 = st.columns([2, 1])

        with col1:
            fig = px.pie(minor_adult_data, values='Count', names='Category',
                         title='Minor vs Adult Distribution',
                         hole=0.5,
                         color_discrete_sequence=['#9b59b6', '#f39c12'])
            fig.update_layout(autosize=True, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Statistics")
            st.metric("Total Minors", f"{total_minors:,}")
            st.metric("Total Adults", f"{total_adults:,}")
            minor_percentage = (total_minors / (total_minors + total_adults)) * 100
            st.metric("Minor Percentage", f"{minor_percentage:.1f}%")

else:
    st.warning("⚠️ Age group data not available in filtered dataset")

st.markdown("---")




# ------------- Comparative Analysis ---------------
st.header("📊 Comparative Analysis")

tab1, tab2 = st.tabs(["State Comparison", "Year-over-Year"])


with tab1:
    st.subheader("Compare Multiple States")
    
    # Select states to compare
    compare_states = st.multiselect(
        "Select states to compare (max 5)",
        options=sorted(filtered_data['state'].unique()),
        default=sorted(filtered_data['state'].unique())[:3],
        max_selections=5
    )
    
    if len(compare_states) > 0:
        compare_data = filtered_data[filtered_data['state'].isin(compare_states)]
        
        # Monthly comparison
        monthly_compare = compare_data.groupby(['state', 'month'])['total_enrollment'].sum().reset_index()
        
        fig = px.line(monthly_compare, x='month', y='total_enrollment', color='state',
                      title='Monthly Enrollment Comparison',
                      markers=True,
                      labels={'total_enrollment': 'Total Enrollment', 'month': 'Month'})
        fig.update_layout(autosize=True, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # State statistics
        state_stats = compare_data.groupby('state')['total_enrollment'].agg(['sum', 'mean', 'median', 'std']).reset_index()
        state_stats.columns = ['State', 'Total', 'Mean', 'Median', 'Std Dev']
        
        st.dataframe(state_stats, use_container_width=True)



with tab2:
    st.subheader("Year-over-Year Analysis")
    
    yearly_data = filtered_data.groupby('year')['total_enrollment'].agg(['sum', 'mean']).reset_index()
    yearly_data.columns = ['Year', 'Total_Enrollment', 'Avg_Enrollment']
    
    if len(yearly_data) > 1:
        # Calculate YoY growth
        yearly_data['Growth_%'] = yearly_data['Total_Enrollment'].pct_change() * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(yearly_data, x='Year', y='Total_Enrollment',
                         title='Total Enrollment by Year',
                         color='Total_Enrollment',
                         color_continuous_scale='Blues')
            fig.update_layout(autosize=True, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(yearly_data, x='Year', y='Growth_%',
                          title='Year-over-Year Growth Rate (%)',
                          markers=True)
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.update_layout(autosize=True, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(yearly_data, use_container_width=True)
    else:
        st.info("ℹ️ Multiple years needed for year-over-year comparison")

st.markdown("---")






# --------------- Data Explorer ---------------
st.header("🔍 Data Explorer")

st.subheader("Raw Data View")

# show/hide columns selector
all_columns = filtered_data.columns.tolist()
selected_columns = st.multiselect(
    "Select columns to display",
    options=all_columns,
    default=all_columns[:10]
)

if len(selected_columns) > 0:
    # Display filtered data
    display_df = filtered_data[selected_columns].head(100)
    st.dataframe(display_df, use_container_width=True)
    
    # Download button
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='aadhaar_enrollment_filtered.csv',
        mime='text/csv',
    )

st.markdown("---")






# -------------- Statistical Summary -----------
st.header("📈 Statistical Summary")

# Select numerical columns
numerical_cols = filtered_data.select_dtypes(include=[np.number]).columns.tolist()

if len(numerical_cols) > 0:
    selected_metric = st.selectbox(
        "Select metric for statistical analysis",
        options=numerical_cols
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Histogram
        fig = px.histogram(filtered_data, x=selected_metric,
                          title=f'Distribution of {selected_metric}',
                          nbins=50,
                          color_discrete_sequence=['steelblue'])
        fig.update_layout(autosize=True, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Statistics
        st.markdown("#### Statistics")
        st.metric("Mean", f"{filtered_data[selected_metric].mean():,.2f}")
        st.metric("Median", f"{filtered_data[selected_metric].median():,.2f}")
        st.metric("Std Dev", f"{filtered_data[selected_metric].std():,.2f}")
        st.metric("Min", f"{filtered_data[selected_metric].min():,.2f}")
        st.metric("Max", f"{filtered_data[selected_metric].max():,.2f}")

st.markdown("---")




# ------------- Footer ---------------
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; padding: 25px; margin-top: 20px;'>
    <p style='color: #333333; font-size: 15px; margin: 8px 0;'>
        <strong>📊 Created & Developed by:</strong> Parth Patel
    </p>
    <p style='color: #555555; font-size: 14px; margin: 5px 0;'>
        💼 Data Analysis | 📈 Visualization | 🔍 Business Intelligence
    </p>
    <p style='color: #666666; font-size: 12px; margin-top: 12px;'>
        © 2025 All Rights Reserved
    </p>
</div>
""",
    unsafe_allow_html=True
)