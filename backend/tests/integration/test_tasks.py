from typing import Any
import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestCreateTask:
    async def test_create_task_returns_200(self, client: AsyncClient) -> None:
        response = await client.post("/api/tasks", json={"title": "Buy milk"})
        assert response.status_code == 200

    async def test_response_contains_fields(self, client: AsyncClient) -> None:
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
    async def test_invalid_payload(self, client: AsyncClient, invalid_payload: dict[str, Any], expected_status: int) -> None:
        response = await client.post("/api/tasks", json=invalid_payload)
        assert response.status_code == expected_status


@pytest.mark.integration
class TestGetTasks:
    async def test_get_all_tasks_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/api/tasks")
        assert response.status_code == 200

    async def test_get_all_tasks_returns_tasks_list(self, client: AsyncClient) -> None:
        await client.post("/api/tasks", json={"title": "Buy milk"})
        response = await client.get("/api/tasks")
        body = response.json()
        assert isinstance(body["tasks"], list)

    async def test_get_all_tasks_returns_empty_when_no_tasks(self, client: AsyncClient) -> None:
        response = await client.get("/api/tasks")
        body = response.json()
        assert response.status_code == 200
        assert body["tasks"] == []


@pytest.mark.integration
class TestUpdateTask:
    async def test_update_task_returns_200(self, client: AsyncClient, sample_task: dict[str, Any]) -> None:
        task_id = sample_task["id"]
        response = await client.patch(f"/api/tasks/{task_id}", json={"title": "Buy water"})
        assert response.status_code == 200

    async def test_update_task_returns_new_title(self, client: AsyncClient, sample_task: dict[str, Any]) -> None:
        task_id = sample_task["id"]
        response = await client.patch(f"/api/tasks/{task_id}", json={"title": "Buy water"})
        body = response.json()
        assert body["title"] == "Buy water"

    async def test_update_task_status_returns_200(self, client: AsyncClient, sample_task: dict[str, Any]) -> None:
        task_id = sample_task["id"]
        response = await client.patch(f"/api/tasks/{task_id}", json={"status": "completed"})
        assert response.status_code == 200

    async def test_update_task_status_returns_completed(self, client: AsyncClient, sample_task: dict[str, Any]) -> None:
        task_id = sample_task["id"]
        response = await client.patch(f"/api/tasks/{task_id}", json={"status": "completed"})
        body = response.json()
        assert body["status"] == "completed"

    async def test_update_nonexistent_task_returns_404(self, client: AsyncClient) -> None:
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = await client.patch(f"/api/tasks/{nonexistent_id}", json={"title": "Buy water"})
        assert response.status_code == 404


@pytest.mark.integration
class TestDeleteTask:
    async def test_delete_task_returns_204(self, client: AsyncClient, sample_task: dict[str, Any]) -> None:
        task_id = sample_task["id"]
        response = await client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204

    async def test_deleted_task_not_in_task_list(self, client: AsyncClient, sample_task: dict[str, Any]) -> None:
        task_id = sample_task["id"]
        await client.delete(f"/api/tasks/{task_id}")
        response = await client.get("/api/tasks")
        assert response.json()["tasks"] == []

    async def test_delete_nonexistent_task_returns_404(self, client: AsyncClient) -> None:
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = await client.delete(f"/api/tasks/{nonexistent_id}")
        assert response.status_code == 404
