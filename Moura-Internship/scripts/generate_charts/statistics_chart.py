import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import statsmodels.api as sm

df = pd.read_csv('data/sample_sales.csv')
df['total'] = df['quantity'] * df['unit_price']
plt.figure(figsize=(8,5))
plt.scatter(df['quantity'], df['total'], color='blue', label='Dados reais')
X = sm.add_constant(df['quantity'])
model = sm.OLS(df['total'], X).fit()
plt.plot(df['quantity'], model.predict(X), color='red', label='OLS')
r, p = pearsonr(df['quantity'], df['total'])
plt.title(f'Pearson r={r:.2f}, p={p:.2g} | OLS R²={model.rsquared:.2f}')
plt.xlabel('Quantidade')
plt.ylabel('Receita Total')
plt.legend()
plt.tight_layout()
plt.savefig('public/statistics.png')
