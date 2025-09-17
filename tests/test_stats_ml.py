import os, requests
BASE = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

def test_pearson():
    r = requests.get(f"{BASE}/stats/pearson", timeout=5)
    assert r.status_code == 200
    js = r.json()
    assert "pearson_r" in js and "p_value" in js

def test_ols():
    r = requests.get(f"{BASE}/stats/ols", timeout=5)
    assert r.status_code == 200
    js = r.json()
    assert "params" in js and "r2" in js

def test_ml_train_predict():
    r = requests.post(f"{BASE}/ml/train", timeout=10)
    assert r.status_code == 200
    pr = requests.post(f"{BASE}/ml/predict", json={"quantity": 10, "unit_price": 200}, timeout=5)
    assert pr.status_code == 200
    js = pr.json()
    assert "y_pred" in js
