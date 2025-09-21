import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/sample_sales.csv')
df['total'] = df['quantity'] * df['unit_price']
plt.figure(figsize=(8,5))
df.groupby('product')['total'].sum().plot(kind='bar', color='skyblue')
plt.title('Receita por Produto (Matplotlib)')
plt.ylabel('Receita Total')
plt.xlabel('Produto')
plt.tight_layout()
plt.savefig('public/matplotlib.png')
