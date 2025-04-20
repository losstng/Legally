import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import models
from app.utils.security import get_current_user, create_access_token

# Fake user for test context
test_user = models.User(
    id=1,
    name="Test User",
    age=30,
    email="test@example.com",
    role="user"
)

# Override auth for tests
def override_get_current_user():
    return test_user

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def async_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")

@pytest.mark.asyncio
async def test_ask_endpoint(async_client):
    async with async_client as client:
        response = await client.post(
            "/ask/ask",
            data={"question": "What is immigration law?"}
        )
    print(response.text)
    assert response.status_code == 200
    json_data = response.json()
    assert "answer" in json_data["data"]

@pytest.mark.asyncio
async def test_ask_without_auth():
    app.dependency_overrides.clear()  # Remove auth override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/ask/ask", json={"question": "Who is a refugee?"})
    print(response.text)
    assert response.status_code == 401