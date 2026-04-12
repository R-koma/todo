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
        assert "created_at" in body
        assert "updated_at" in body
    
    @pytest.mark.parametrize("invalid_payload, expected_status", [
        ({"title": ""}, 422),
        ({"title": None}, 422),
        ({}, 422)
    ])
    async def test_invalid_payload(self, client, invalid_payload, expected_status):
        response = await client.post("/api/tasks", json=invalid_payload)
        assert response.status_code == expected_status
    

@pytest.mark.integration
class TestGetTasks:
    async def test_get_all_tasks_returns_200(self, client):
        response = await client.get("/api/tasks")
        assert response.status_code == 200

    async def test_get_all_tasks_returns_tasks_list(self, client):
        await client.post("/api/tasks", json={"title": "Buy milk"})
        response = await client.get("/api/tasks")
        body = response.json()
        assert isinstance(body["tasks"], list)

    async def test_get_all_tasks_returns_empty_when_no_tasks(self, client):
        response = await client.get("/api/tasks")
        body = response.json()
        assert response.status_code == 200
        assert body["tasks"] == []
