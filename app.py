import streamlit as st
import pandas as pd
import plotly.express as px

# First Chart title
st.title("Nassau Candy Distributor")
st.subheader("Product Profitability Analysis")

# Load the data
Product_data = pd.read_csv(r"C:\Users\user\Documents\GitHub\Unified-Mentor-Project-1\Groupby Product Name.csv")

# sort products in descending order of profit
top_products = Product_data.sort_values(by = 'Gross Profit', ascending = False)

# Create a bar chart
fig1 = px.bar(top_products, x = 'Gross Profit', y = 'Product Name', 
               text = 'Gross Profit', title = 'Top Products by Profit')
fig1.update_layout( height= 600, bargap = 0.2)
fig1.update_traces(texttemplate = '$%{text:.2f}')
# Dispaly the Chart
st.plotly_chart(fig1, use_container_width=True)

# Create a scatter plot
fig2 = px.scatter(Product_data, x = 'Sales', y = 'Gross Margin %', hover_name  = 'Product Name',
                 color = 'Gross Margin %', title = 'Sales vs Gross Margin %')
fig2.update_layout(height = 600)
# Display the chart
st.plotly_chart(fig2, use_container_width = True)


st.subheader("Division Performance Analysis")
# Load the data
Division_data = pd.read_csv(r"C:\Users\user\Documents\GitHub\Unified-Mentor-Project-1\Groupby Division.csv")

# Create a clustered bar chart
fig3 = px.bar(Division_data, x = 'Division', y = ['Sales', 'Gross Profit'], barmode = 'group', 
              title = 'Sales and Gross Profit by Division')
fig3.update_layout(xaxis_title = 'Division', yaxis_title = 'Amount ($)', height = 1000,title_x = 0.25)
fig3.update_yaxes(tickprefix = '$')

#Display the chart
st.plotly_chart(fig3, use_container_width = True)

# Create a boxplot
fig4 = px.box(Product_data, x = 'Gross Margin %', y = 'Product Name', color = 'Division'
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