#export PYTHONPATH=$(pwd)
#pytest
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app
from app.db import models
from app.utils.security import get_current_user
from app.utils import redis

# Fake user to inject
test_user = models.User(
    id=1,
    name="Test User",
    age=30,
    email="test@example.com",
    role="user"
)

# Override the dependency
def override_get_current_user():
    return test_user

app.dependency_overrides = {}
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_ask_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/ask/ask",
            json={"question": "What is immigration law?"}
        )

    assert response.status_code == 200
    assert "answer" in response.json()