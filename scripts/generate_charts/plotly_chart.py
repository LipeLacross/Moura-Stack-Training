import pandas as pd
import plotly.express as px

df = pd.read_csv('data/sample_sales.csv')
df['total'] = df['quantity'] * df['unit_price']
fig = px.bar(df, x='product', y='total', color='region', title='Receita por Produto (Plotly)')
fig.write_image('public/plotly.png')

# Renomeado para evitar conflito com biblioteca plotly
