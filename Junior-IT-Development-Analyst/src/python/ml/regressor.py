import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "ml" / "models"
MODEL_PATH = MODEL_DIR / "regressor.pkl"


def generate_sample_data(n_samples: int = 1000):
    rng = np.random.default_rng(42)
    X = rng.standard_normal((n_samples, 4))
    y = 100 + X[:, 0] * 15 + X[:, 1] * 8 + X[:, 2] * -5 + X[:, 3] * 3 + rng.normal(0, 5, n_samples)
    feature_names = ["temp_ambiente", "umidade", "velocidade_producao", "qualidade_insumo"]
    return X, y, feature_names


def train():
    X, y, feature_names = generate_sample_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
        "mae": round(float(mean_absolute_error(y_test, y_pred)), 4),
        "r2": round(float(r2_score(y_test, y_pred)), 4),
        "feature_importance": dict(zip(feature_names, model.feature_importances_.round(4))),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return metrics


def predict_regression(features: list[float]):
    if not MODEL_PATH.exists():
        train()
    model = joblib.load(MODEL_PATH)
    X = np.array(features).reshape(1, -1)
    pred = round(float(model.predict(X)[0]), 2)
    importance = dict(zip(
        ["temp_ambiente", "umidade", "velocidade_producao", "qualidade_insumo"],
        model.feature_importances_.round(4),
    ))
    return pred, importance


if __name__ == "__main__":
    metrics = train()
    print("Regressor treinado com sucesso!")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
