"""Tests for task endpoints."""

import pytest


@pytest.mark.asyncio
async def test_create_and_list_task(app, auth_headers):
    resp = await app.post(
        "/api/v1/tasks",
        json={"title": "Build feature X", "assignee": "kimi", "priority": "high"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"].startswith("task-")
    assert data["assignee"] == "kimi"
    assert data["status"] == "pending"

    resp2 = await app.get("/api/v1/tasks?agent=kimi", headers=auth_headers)
    assert resp2.status_code == 200
    tasks = resp2.json()
    assert any(t["id"] == data["id"] for t in tasks)


@pytest.mark.asyncio
async def test_update_task_status(app, auth_headers):
    resp = await app.post(
        "/api/v1/tasks",
        json={"title": "Update test task"},
        headers=auth_headers,
    )
    task_id = resp.json()["id"]

    resp2 = await app.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "in_progress"},
        headers=auth_headers,
    )
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_get_task_by_id(app, auth_headers):
    resp = await app.post(
        "/api/v1/tasks",
        json={"title": "Get test task", "description": "Full description"},
        headers=auth_headers,
    )
    task_id = resp.json()["id"]

    resp2 = await app.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert resp2.status_code == 200
    assert resp2.json()["description"] == "Full description"
