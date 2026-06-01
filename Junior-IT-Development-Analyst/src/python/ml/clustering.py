import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "ml" / "models"
MODEL_PATH = MODEL_DIR / "cluster.pkl"
SCALER_PATH = MODEL_DIR / "cluster_scaler.pkl"


def generate_sample_data(n_samples: int = 500):
    rng = np.random.default_rng(42)

    c1 = rng.normal(loc=[10, 10, 10], scale=2, size=(n_samples // 3, 3))
    c2 = rng.normal(loc=[25, 30, 20], scale=2, size=(n_samples // 3, 3))
    c3 = rng.normal(loc=[40, 15, 35], scale=2, size=(n_samples // 3, 3))

    X = np.vstack([c1, c2, c3])
    feature_names = ["consumo_energia", "horas_operacao", "temp_media"]
    return X, feature_names


def train(n_clusters: int = 3):
    X, feature_names = generate_sample_data()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)

    sil_score = silhouette_score(X_scaled, labels)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    return {
        "silhouette_score": round(float(sil_score), 4),
        "n_clusters": n_clusters,
        "inertia": round(float(model.inertia_), 2),
        "cluster_centers": model.cluster_centers_.round(2).tolist(),
    }


def predict_cluster(features: list[float]):
    if not MODEL_PATH.exists():
        train()
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    cluster_id = int(model.predict(X_scaled)[0])

    dist = model.transform(X_scaled)[0]
    similarity = round(float(1 / (1 + dist[cluster_id])), 4)
    return cluster_id, similarity


if __name__ == "__main__":
    metrics = train()
    print("KMeans treinado com sucesso!")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
