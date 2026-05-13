import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Nassau Candy Distributor")
# First Chart title
st.subheader("Product Profitability Analysis")

# Load the data
filtered_data = pd.read_csv(r"C:\Users\user\Documents\GitHub\Unified-Mentor-Project-1\Filter by date.csv")

# filters
st.sidebar.header("Filters")

# division filter
st.sidebar.subheader("Division Filter")
division_filter = st.sidebar.multiselect(
    "Select Division",
    options=filtered_data['Division'].unique(),
    default=filtered_data['Division'].unique())
filtered_data = filtered_data[filtered_data['Division'].isin(division_filter)]

# product filter
st.sidebar.subheader("Product Filter")
product_filter = st.sidebar.multiselect(
    "Select Product",
    options=filtered_data['Product Name'].unique(),
    default=filtered_data['Product Name'].unique())
filtered_data = filtered_data[filtered_data['Product Name'].isin(product_filter)]

# Date filter
st.sidebar.subheader("Date Filter")
filtered_data['Order Date'] = pd.to_datetime(filtered_data['Order Date'])
date_range = st.sidebar.date_input("Select Date Range", [filtered_data['Order Date'].min(), filtered_data['Order Date'].max()])
start_date = pd.to_datetime(date_range[0])  
end_date = pd.to_datetime(date_range[1])        
filtered_data = filtered_data[(filtered_data['Order Date'] >= start_date) & (filtered_data['Order Date'] <= end_date)]


#Product_data
new_data = filtered_data.groupby(['Product Name','Division']).agg(
    {'Cost':'sum','Sales':'sum','Units':'sum','Gross Profit':'sum'}).reset_index()
new_data['Gross Margin %'] = ((new_data['Gross Profit']/new_data['Sales'])*100).round(2)
new_data['Profit Per Unit'] = (new_data['Gross Profit']/new_data['Units']).round(2)
Total_Sales = new_data['Sales'].sum()
new_data['Revenue Contribution'] = ((new_data['Sales']/Total_Sales)*100).round(2)
new_data['Profit contribution'] = ((new_data['Gross Profit']/(new_data['Gross Profit'].sum()))*100).round(2)
# sort products in descending order of profit
top_products = new_data.sort_values(by = 'Gross Profit', ascending = False)

#Division Data
division_data = filtered_data.groupby('Division').agg({
    'Cost':'sum','Sales':'sum','Units':'sum','Gross Profit':'sum'}).reset_index()
division_data['Gross Margin %'] = ((division_data['Gross Profit']/division_data['Sales'])*100).round(2)
division_data['Profit Per Unit'] = ((division_data['Gross Profit']/division_data['Units'])*100).round(2)
division_data['Revenue Contribution'] = (division_data['Sales']/(division_data['Sales'].sum())*100).round(2)
division_data['Profit contribution'] = (division_data['Gross Profit']/(division_data['Gross Profit'].sum())*100).round(2)


# Create a bar chart
fig1 = px.bar(top_products, x = 'Gross Profit', y = 'Product Name', 
               text = 'Gross Profit', title = 'Top Products by Profit')
fig1.update_layout( height= 600, bargap = 0.2)
fig1.update_traces(texttemplate = '$%{text:.2f}')
# Dispaly the Chart
st.plotly_chart(fig1, use_container_width=True)

# Create a scatter plot
fig2 = px.scatter(new_data, x = 'Sales', y = 'Gross Margin %', hover_name  = 'Product Name',
                 color = 'Gross Margin %', title = 'Sales vs Gross Margin %')
fig2.update_layout(height = 600)
# Display the chart
st.plotly_chart(fig2, use_container_width = True)


st.subheader("Division Performance Analysis")

# Create a clustered bar chart
fig3 = px.bar(division_data, x = 'Division', y = ['Sales', 'Gross Profit'], barmode = 'group', 
              title = 'Sales and Gross Profit by Division')
fig3.update_layout(xaxis_title = 'Division', yaxis_title = 'Amount ($)', height = 1000,title_x = 0.25)
fig3.update_yaxes(tickprefix = '$')

#Display the chart
st.plotly_chart(fig3, use_container_width = True)

# Create a boxplot
fig4 = px.box(new_data, x = 'Gross Margin %', y = 'Product Name', color = 'Division'
              , title = 'Gross Margin Distribution by Division', points = 'all')
fig4.update_layout(yaxis_title = 'Product Name', height = 600, title_x = 0.3)
# Display the chart
st.plotly_chart(fig4, use_container_width = True)

# Pareto analysis
import plotly.graph_objects as go
fig5 = go.Figure()
# Bar chart
fig5.add_trace(go.Bar(y = top_products['Gross Profit'], x = top_products['Product Name'], 
                      name = 'Gross Profit', width = 0.8))
# Cumulative line
fig5.add_trace(go.Scatter(y = top_products['Profit contribution'], x = top_products['Product Name'],
                          yaxis = 'y2',line=dict(color = 'red', width = 3),name = 'Cumulative %', 
                          mode = 'lines+markers'))
# Layout
fig5.update_layout(title = 'Pareto Analysis of Products',height = 1000, width = 1300, yaxis_title = 'Gross Profit ($)',
                   yaxis2 = dict(overlaying = 'y', side = 'top', range = [0,100]), xaxis_title
                   = 'Product Name')
fig5.add_hline(y=80, line_dash = 'dash', line_color = 'green', annotation_text = '80% Threshold',
           yref = 'y2')
# Display the chart
st.plotly_chart(fig5, use_container_width=True)