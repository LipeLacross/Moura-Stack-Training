import pandas as pd
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

df = pd.read_csv('data/sample_sales.csv')
df['total'] = df['quantity'] * df['unit_price']
spark = SparkSession.builder.master('local[*]').appName('SalesAgg').getOrCreate()
sdf = spark.createDataFrame(df)
agg = sdf.groupBy('product').sum('total').toPandas()
spark.stop()
plt.figure(figsize=(8,5))
agg = agg.rename(columns={'sum(total)': 'total_revenue'})
agg.plot(x='product', y='total_revenue', kind='bar', color='orange', legend=False)
plt.title('Receita Total por Produto (PySpark)')
plt.ylabel('Receita Total')
plt.xlabel('Produto')
plt.tight_layout()
plt.savefig('public/pyspark_agg.png')

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv('data/sample_sales.csv')
df['total'] = df['quantity'] * df['unit_price']
X = df[['quantity']]
y = df['total']
model = LinearRegression().fit(X, y)
pred = model.predict(X)
plt.figure(figsize=(8,5))
plt.scatter(df['quantity'], df['total'], color='blue', label='Dados reais')
plt.plot(df['quantity'], pred, color='red', label='Regressão Linear')
plt.xlabel('Quantidade')
plt.ylabel('Receita Total')
plt.title('Regressão Linear: Receita vs Quantidade')
plt.legend()
plt.tight_layout()
plt.savefig('public/ml_regression.png')
