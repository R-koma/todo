import pytest


@pytest.mark.integration
class TestCreateTask:
    async def test_create_task_returns_200(self, client):
        response = await client.post("/api/tasks", json={"title": "Buy milk"})
        assert response.status_code == 200

    async def test_response_contains_fields(self, client):
        response = await client.post("/api/tasks", json={"title": "Buy milk"})
        body = response.json()
        assert body["title"] == "Buy milk"
        assert body["status"] == "in_progress"
        assert "id" in body
    
    @pytest.mark.parametrize("invalid_payload, expected_status", [
        ({"title": ""}, 422),
        ({"title": None}, 422),
        ({}, 422)
    ])
    async def test_invalid_payload(self, client, invalid_payload, expected_status):
        response = await client.post("/api/tasks", json=invalid_payload)
        assert response.status_code == expected_status
