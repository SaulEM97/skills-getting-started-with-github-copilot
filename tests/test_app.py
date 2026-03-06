import pytest
from httpx import AsyncClient
from fastapi import status
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange: create test client
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: make GET request to /activities
        response = await ac.get("/activities")
    # Assert: check response
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

@pytest.mark.asyncio
async def test_signup_for_activity_success():
    # Arrange: get an activity name and test email
    async with AsyncClient(app=app, base_url="http://test") as ac:
        activities_resp = await ac.get("/activities")
        activities = activities_resp.json()
        activity_name = next(iter(activities))
        email = "testuser@example.com"
        # Act: post signup
        response = await ac.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert: check response
    assert response.status_code == status.HTTP_200_OK
    assert "Signed up" in response.json().get("message", "")

@pytest.mark.asyncio
async def test_signup_for_activity_not_found():
    # Arrange: use a non-existent activity
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: post signup to invalid activity
        response = await ac.post("/activities/invalid_activity/signup", params={"email": "user@example.com"})
    # Assert: check 404
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_root_redirect():
    # Arrange: create test client
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: get root
        response = await ac.get("/")
    # Assert: check redirect
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_307_TEMPORARY_REDIRECT)
    # Optionally, check the final URL
    # assert response.url.path == "/static/index.html"
