from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with patch(
        "app.main.connect_db",
        new_callable=AsyncMock,
    ), patch(
        "app.main.close_db",
        new_callable=AsyncMock,
    ):
        with TestClient(app) as client:
            response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "Naukri AI Agent is running",
    }