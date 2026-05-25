import pytest
from unittest.mock import patch, AsyncMock

class TestSummaryRoute:
    def test_summary_success(self, client, auth_headers, created_project):
        # Create a task first so there's something to summarise
        client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json={"title": "Build login page", "priority": "high"},
            headers=auth_headers
        )

        mock_response = AsyncMock()
        mock_response.json.return_value = {"response": "The project is progressing well."}
        mock_response.raise_for_status = AsyncMock()

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            response = client.post(
                f"/api/projects/{created_project['id']}/summary",
                headers=auth_headers
            )

        assert response.status_code == 200
        assert "summary" in response.json()
        assert response.json()["summary"] == "The project is progressing well."

    def test_summary_no_tasks(self, client, auth_headers, created_project):
        mock_response = AsyncMock()

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            response = client.post(
                f"/api/projects/{created_project['id']}/summary",
                headers=auth_headers
            )

        assert response.status_code == 400
        assert "No tasks" in response.json()["detail"]

    def test_summary_ollama_unreachable(self, client, auth_headers, created_project):
        import httpx
        client.post(
            f"/api/projects/{created_project['id']}/tasks",
            json={"title": "Some task", "priority": "low"},
            headers=auth_headers
        )

        with patch("httpx.AsyncClient.post", side_effect=httpx.ConnectError("unreachable")):
            response = client.post(
                f"/api/projects/{created_project['id']}/summary",
                headers=auth_headers
            )

        assert response.status_code == 503

    def test_summary_project_not_found(self, client, auth_headers):
        response = client.post("/api/projects/99999/summary", headers=auth_headers)
        assert response.status_code == 404

    def test_summary_unauthenticated(self, client, created_project):
        response = client.post(f"/api/projects/{created_project['id']}/summary")
        assert response.status_code in (401, 403)