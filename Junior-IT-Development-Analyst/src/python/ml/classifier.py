import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "ml" / "models"
MODEL_PATH = MODEL_DIR / "classifier.pkl"


def generate_sample_data(n_samples: int = 1000):
    rng = np.random.default_rng(42)
    X = rng.standard_normal((n_samples, 5))
    y = (X[:, 0] * 0.5 + X[:, 1] * 0.3 + X[:, 2] * -0.2 + rng.normal(0, 0.3, n_samples) > 0).astype(int)
    feature_names = ["temperatura", "vibracao", "pressao", "horas_operacao", "carga"]
    return X, y, feature_names


def train():
    X, y, feature_names = generate_sample_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "feature_importance": dict(zip(feature_names, model.feature_importances_.round(4))),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return metrics


def predict_classification(features: list[float]):
    if not MODEL_PATH.exists():
        train()
    model = joblib.load(MODEL_PATH)
    X = np.array(features).reshape(1, -1)
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][1])
    importance = dict(zip(
        ["temperatura", "vibracao", "pressao", "horas_operacao", "carga"],
        model.feature_importances_.round(4),
    ))
    return pred, prob, importance


if __name__ == "__main__":
    metrics = train()
    print("Modelo treinado com sucesso!")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
