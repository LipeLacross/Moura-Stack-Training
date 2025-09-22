import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Dados simulados
np.random.seed(42)
X = np.arange(1, 21).reshape(-1, 1)
Y = 2.5 * X.flatten() + np.random.normal(0, 10, size=X.shape[0])

# Modelo de regressão
model = LinearRegression()
model.fit(X, Y)
Y_pred = model.predict(X)

# Plot
plt.figure(figsize=(8, 5))
plt.scatter(X, Y, color='blue', label='Dados reais')
plt.plot(X, Y_pred, color='red', linewidth=2, label='Regressão Linear')
plt.title('Regressão Linear — Vendas Simuladas')
plt.xlabel('Quantidade')
plt.ylabel('Receita')
plt.legend()
plt.tight_layout()

# Salvar imagem
plt.savefig(r'E:/8. Programming/Moura-Stack-Training/public/ml_regression.png', dpi=120)
plt.close()
