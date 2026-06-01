from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.python.api.main import app

client = TestClient(app)


class TestHealth:
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data


class TestProcessesAPI:
    def test_create_process(self):
        response = client.post("/api/processes/", json={
            "name": "Teste Automatizado",
            "description": "Processo de teste",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Teste Automatizado"
        assert "id" in data

    def test_list_processes(self):
        response = client.get("/api/processes/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_process_not_found(self):
        response = client.get("/api/processes/9999")
        assert response.status_code == 404


class TestIntegrationAPI:
    def test_sync_systems(self):
        response = client.post("/api/integration/sync", json={
            "source_system": "sap",
            "target_system": "powerbi",
            "payload": {"items": [{"id": 1, "name": "test"}]},
            "action": "sync",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["records_processed"] == 1

    def test_list_systems(self):
        response = client.get("/api/integration/systems")
        assert response.status_code == 200
        data = response.json()
        assert "available" in data


class TestMLAPI:
    def test_predict_invalid_model(self):
        response = client.post("/api/ml/predict", json={
            "features": [1.0, 2.0, 3.0, 4.0, 5.0],
            "model_type": "invalid",
        })
        assert response.status_code == 400
