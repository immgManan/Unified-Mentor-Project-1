top_products = Products_data.sort_values(by = 'Gross Profit', ascending = False)
fig = px.bar(top_products, x = 'Product Name',y = 'Gross Profit', orientation = 'h',title ='Products by Profit',text = 'Gross Profit')
st.plotly_chart(fig)
