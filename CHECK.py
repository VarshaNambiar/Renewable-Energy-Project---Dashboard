import pandas as pd
import streamlit as st
import plotly.express as px

# Load data from the Excel file
df = pd.read_excel('renewable_projects.xlsx')

# Replace hyphens with NaN in the 'End Date' column
df['End Date'] = df['End Date'].replace('-', pd.NaT)

# Calculate Financial KPIs dynamically
df['Efficiency (USD/MWh)'] = df['Profit (USD)'] / df['Energy Generated (MWh)']  # Formula: Profit / Energy Generated
df['Gross Margin (%)'] = (df['Profit (USD)'] / df['Revenue (USD)']) * 100  # Formula: (Profit / Revenue) * 100
df['Cost Efficiency (USD/MWh)'] = df['Operational Cost'] / df['Energy Generated (MWh)']  # Formula: Operational Cost / Energy Generated
df['ROI (%)'] = (df['Profit (USD)'] / df['Operational Cost']) * 100  # Formula: (Profit / Operational Cost) * 100
df['Revenue per MWh (USD)'] = df['Revenue (USD)'] / df['Energy Generated (MWh)']  # Formula: Revenue / Energy Generated

# Initialize Streamlit app
st.set_page_config(page_title="Renewable Energy Projects Dashboard", page_icon="🌍", layout="wide")

# Create KPIs
st.title("Renewable Energy Projects Dashboard")
st.write("A comprehensive dashboard providing insights into energy generation, revenue, CO2 reduction, and more.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Key Insights"])

# Filters for Region, Energy Type, and Project Name
region_filter = st.sidebar.multiselect('Select Region', df['Location'].unique())
energy_type_filter = st.sidebar.multiselect('Select Energy Type', df['Energy Type'].unique())
project_name_filter = st.sidebar.multiselect('Select Project', df['Project Name'].unique())

# Filter the dataframe based on selected slicers
filtered_df = df.copy()

if region_filter:
    filtered_df = filtered_df[filtered_df['Location'].isin(region_filter)]

if energy_type_filter:
    filtered_df = filtered_df[filtered_df['Energy Type'].isin(energy_type_filter)]

if project_name_filter:
    filtered_df = filtered_df[filtered_df['Project Name'].isin(project_name_filter)]

# Key Insights Page
if page == "Key Insights":
    st.header("Key Insights")
    
    st.write("### 1. Overview of KPIs and Calculations")
    st.write("""
    - **Efficiency (USD/MWh)**: Profit generated per MWh of energy generated.
      - Formula: Profit / Energy Generated (MWh)
    - **Gross Margin (%)**: Percentage of revenue that is gross profit.
      - Formula: (Profit / Revenue) * 100
    - **Cost Efficiency (USD/MWh)**: Operational cost incurred per MWh of energy generated.
      - Formula: Operational Cost / Energy Generated (MWh)
    - **ROI (%)**: Return on investment from the operational cost.
      - Formula: (Profit / Operational Cost) * 100
    - **Revenue per MWh (USD)**: Revenue generated per MWh of energy produced.
      - Formula: Revenue / Energy Generated (MWh)
    """)
    
    st.write("### 2. Key Insights from the Data")

    # Insights: Energy Generation
    max_energy_type = filtered_df.groupby('Energy Type')['Energy Generated (MWh)'].sum().idxmax()
    max_energy_value = filtered_df.groupby('Energy Type')['Energy Generated (MWh)'].sum().max()
    st.write(f"**Energy Generation Insight:**")
    st.write(f"- {max_energy_type} projects contribute the most to energy generation with a total of {max_energy_value:,.0f} MWh.")
    
    # Insights: Revenue
    max_revenue_type = filtered_df.groupby('Energy Type')['Revenue (USD)'].sum().idxmax()
    max_revenue_value = filtered_df.groupby('Energy Type')['Revenue (USD)'].sum().max()
    st.write(f"**Revenue Insight:**")
    st.write(f"- {max_revenue_type} projects contribute the most to revenue, generating a total of ${max_revenue_value:,.0f}.")
    
    # Insights: CO2 Reduction
    max_co2_type = filtered_df.groupby('Energy Type')['CO2 Reduction (tons)'].sum().idxmax()
    max_co2_value = filtered_df.groupby('Energy Type')['CO2 Reduction (tons)'].sum().max()
    st.write(f"**CO2 Reduction Insight:**")
    st.write(f"- {max_co2_type} projects contribute the most to CO2 reduction, with a total of {max_co2_value:,.0f} tons of CO2 reduced.")
    
    # Insights: Profit
    max_profit_type = filtered_df.groupby('Energy Type')['Profit (USD)'].sum().idxmax()
    max_profit_value = filtered_df.groupby('Energy Type')['Profit (USD)'].sum().max()
    st.write(f"**Profit Insight:**")
    st.write(f"- {max_profit_type} projects contribute the most to profit, generating a total of ${max_profit_value:,.0f}.")
    
    # Insights: Installed Capacity
    max_capacity_project = filtered_df.loc[filtered_df['Installed Capacity (MW)'].idxmax()]
    st.write(f"**Installed Capacity Insight:**")
    st.write(f"- The project with the largest installed capacity is {max_capacity_project['Project Name']} with {max_capacity_project['Installed Capacity (MW)']} MW.")
    
    # Insights: Project Status
    operational_projects = filtered_df[filtered_df['Project Status'] == 'Operational']
    under_construction_projects = filtered_df[filtered_df['Project Status'] == 'Under Construction']
    planned_projects = filtered_df[filtered_df['Project Status'] == 'Planned']
    st.write(f"**Project Status Insight:**")
    st.write(f"- There are {len(operational_projects)} operational projects, {len(under_construction_projects)} under construction, and {len(planned_projects)} planned projects.")

    # Insights: Efficiency
    max_efficiency_project = filtered_df.loc[filtered_df['Efficiency (USD/MWh)'].idxmax()]
    st.write(f"**Efficiency Insight:**")
    st.write(f"- The project with the highest efficiency is {max_efficiency_project['Project Name']} with an efficiency of {max_efficiency_project['Efficiency (USD/MWh)']:.2f} USD/MWh.")
    
    # Insights: Gross Margin
    max_margin_project = filtered_df.loc[filtered_df['Gross Margin (%)'].idxmax()]
    st.write(f"**Gross Margin Insight:**")
    st.write(f"- The project with the highest gross margin is {max_margin_project['Project Name']} with a gross margin of {max_margin_project['Gross Margin (%)']:.2f}%.")
    
    # Insights: ROI
    max_roi_project = filtered_df.loc[filtered_df['ROI (%)'].idxmax()]
    st.write(f"**ROI Insight:**")
    st.write(f"- The project with the highest ROI is {max_roi_project['Project Name']} with an ROI of {max_roi_project['ROI (%)']:.2f}%.")

# Dashboard Page
if page == "Dashboard":
    st.header("Dashboards")

    # Calculating the KPIs for the filtered data
    total_energy = filtered_df['Energy Generated (MWh)'].sum()
    total_revenue = filtered_df['Revenue (USD)'].sum()
    total_co2_reduction = filtered_df['CO2 Reduction (tons)'].sum()
    total_profit = filtered_df['Profit (USD)'].sum()

    st.metric("Total Energy Generated (MWh)", total_energy)
    st.metric("Total Revenue (USD)", total_revenue)
    st.metric("Total CO2 Reduction (tons)", total_co2_reduction)
    st.metric("Total Profit (USD)", total_profit)

    # Bar Chart: Energy generated by energy type
    energy_type_bar_chart = px.bar(filtered_df, x='Energy Type', y='Energy Generated (MWh)', title='Energy Generated by Energy Type')
    st.plotly_chart(energy_type_bar_chart)

    # Pie Chart: Revenue by energy type
    revenue_by_type_pie_chart = px.pie(filtered_df, names='Energy Type', values='Revenue (USD)', title='Revenue by Energy Type')
    st.plotly_chart(revenue_by_type_pie_chart)

    # Table: Project-wise details (Energy Generated, Revenue, CO2 Reduction)
    st.write("## Project-wise Details")
    project_details = filtered_df[['Project Name', 'Energy Generated (MWh)', 'Revenue (USD)', 'CO2 Reduction (tons)', 'Profit (USD)']]
    st.dataframe(project_details)

    # Line Chart: Energy generated over time
    energy_line_chart = px.line(filtered_df, x='Start Date', y='Energy Generated (MWh)', color='Energy Type', title='Energy Generation Over Time')
    st.plotly_chart(energy_line_chart)

    # ROI by Project (Scatter Plot)
    st.write("## ROI by Project")
    roi_by_project_scatter = px.scatter(filtered_df, x='Project Name', y='ROI (%)', title='ROI by Project')
    st.plotly_chart(roi_by_project_scatter)

    # Gross Margin by Project (Heatmap or Bubble Chart)
    st.write("## Gross Margin by Project")
    gross_margin_by_project_heatmap = px.density_heatmap(filtered_df, x='Project Name', y='Gross Margin (%)', title='Gross Margin Heatmap')
    st.plotly_chart(gross_margin_by_project_heatmap)

    # CO2 Reduction by Project (Bar Chart)
    st.write("## CO2 Reduction by Project")
    co2_by_project_fig = px.bar(filtered_df, x='Project Name', y='CO2 Reduction (tons)', title='CO2 Reduction by Project')
    st.plotly_chart(co2_by_project_fig)

    # Efficiency vs Revenue (Scatter Plot)
    st.write("## Efficiency vs Revenue")
    efficiency_revenue_scatter = px.scatter(filtered_df, x='Efficiency (USD/MWh)', y='Revenue (USD)', color='Energy Type', title='Efficiency vs Revenue')
    st.plotly_chart(efficiency_revenue_scatter)

    # Sunburst Chart: Energy Generation by Energy Type and Project
    st.write("## Energy Generation by Energy Type and Project")
    sunburst_chart = px.sunburst(filtered_df, path=['Energy Type', 'Project Name'], values='Energy Generated (MWh)', title='Energy Generation by Energy Type and Project')
    st.plotly_chart(sunburst_chart)

    # Bubble Chart: Revenue vs CO2 Reduction
    st.write("## Revenue vs CO2 Reduction")
    revenue_co2_bubble_chart = px.scatter(filtered_df, x='Revenue (USD)', y='CO2 Reduction (tons)', size='Energy Generated (MWh)', color='Energy Type', title='Revenue vs CO2 Reduction')
    st.plotly_chart(revenue_co2_bubble_chart)

    # Operational Insights
    st.write("## Project Status Insights")
    status_distribution_fig = px.bar(filtered_df, x='Project Status', y='Project Name', title='Project Status Distribution', orientation='h')
    st.plotly_chart(status_distribution_fig)

    # Efficiency Insights
    st.write("## Efficiency Insights")
    efficiency_by_project_fig = px.bar(filtered_df, x='Project Name', y='Efficiency (USD/MWh)', title='Efficiency by Project')
    st.plotly_chart(efficiency_by_project_fig)

    st.write("Gross Margin by Project:")
    gross_margin_by_project_fig = px.bar(filtered_df, x='Project Name', y='Gross Margin (%)', title='Gross Margin by Project')
    st.plotly_chart(gross_margin_by_project_fig)

    st.write("Cost Efficiency by Project:")
    cost_efficiency_by_project_fig = px.bar(filtered_df, x='Project Name', y='Cost Efficiency (USD/MWh)', title='Cost Efficiency by Project')
    st.plotly_chart(cost_efficiency_by_project_fig)

    st.write("ROI by Project:")
    roi_by_project_fig = px.bar(filtered_df, x='Project Name', y='ROI (%)', title='ROI by Project')
    st.plotly_chart(roi_by_project_fig)
