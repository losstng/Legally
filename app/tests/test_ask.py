#docker run -d -p 6379:6379 redis
#export PYTHONPATH=$(pwd)
#pytest
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app
from app.db import models
from app.utils.security import get_current_user, create_refresh_token, create_access_token
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

@pytest.fixture
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: test_user
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def auth_token():
    return create_access_token({"email": test_user.email, "role": test_user.role})

@pytest.mark.asyncio #It is a pytest marker to mark it as the REAL test that awaits pytest to execute, the others before were not as needed as this
async def test_ask_endpoint(async_client, override_auth):
    async with async_client as client:
        response = await client.post(  # << use 'client' not 'async_client'
            "/ask/ask", #“Pause here, run this coroutine to completion, and give me the result.”
            json={"question": "What is immigration law?"}
        )
    assert response.status_code == 200 #assert - used to verify that a condition holds true
    assert "answer" in response.json() #if not then it raise Assertion there fore failling the test


@pytest.mark.asyncio
async def test_ask_empty_question(async_client, auth_token):
    async with async_client as client:
        response = await client.post(  # << same here
            "/ask/ask",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"question": ""}
        )
    assert response.status_code in (400, 422)


@pytest.mark.asyncio
async def test_ask_without_auth():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/ask/ask", json={"question": "Who is a refugee?"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ask_without_auth():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/ask/ask", json={"question": "Who is a refugee?"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_ask_history_returns_previous():
    # Create valid token and override auth
    token = create_access_token({"email": "historyuser@example.com", "role": "user"})
    test_user.email = "historyuser@example.com"
    app.dependency_overrides[get_current_user] = lambda: test_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Ask a question to store in DB
        ask_response = await ac.post(
            "/ask/ask",
            headers={"Authorization": f"Bearer {token}"},
            json={"question": "Test history question?"}
        )
        assert ask_response.status_code == 200

        # Fetch the conversation history
        history_response = await ac.get(
            "/ask/history",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert history_response.status_code == 200
    history = history_response.json()
    assert isinstance(history, list) #make sure that history is a list, essentially make sure it is something
    assert any("Test history question?" in item["question"] for item in history) 
    #checks if at least 1 or any is in there, any is just 'has it showed up at least once.