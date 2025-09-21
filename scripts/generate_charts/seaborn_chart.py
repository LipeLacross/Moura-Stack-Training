import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/sample_sales.csv')
df['total'] = df['quantity'] * df['unit_price']
plt.figure(figsize=(8,5))
sns.barplot(data=df, x='product', y='total', hue='region')
plt.title('Receita por Produto (Seaborn)')
plt.ylabel('Receita Total')
plt.xlabel('Produto')
plt.tight_layout()
plt.savefig('public/seaborn.png')
