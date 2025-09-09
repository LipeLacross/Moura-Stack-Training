import os, requests
BASE = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

def test_health():
    r = requests.get(f"{BASE}/health", timeout=5)
    assert r.status_code == 200
    js = r.json()
    assert js["status"] == "ok"

def test_summary():
    r = requests.get(f"{BASE}/metrics/summary", timeout=5)
    assert r.status_code == 200
    js = r.json()
    assert "total_revenue" in js and "top_products" in js
