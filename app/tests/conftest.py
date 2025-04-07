# tests/conftest.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import models
from app.utils.security import create_access_token, get_current_user
from app.utils import redis
#not a test file, essentially a central place to store useable fixture, u will notice that not one calls a real function

#The global utility layer for all tests in this suite.
@pytest.fixture #fixture = preparation before the test, the information needed for the test
def test_user():
    return models.User(
        id=1,
        name="Test User",
        age=30,
        email="testuser@example.com",
        role="user"
    )


@pytest.fixture
def override_auth(test_user): #overriding dependecy
    app.dependency_overrides[get_current_user] = lambda: test_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(test_user): #creating token after overriding dependency
    return create_access_token({"email": test_user.email, "role": test_user.role})


@pytest.fixture
async def async_client(): 
    transport = ASGITransport(app=app) #The AsyncClient will speak directly to your FastAPI app in-memory, using the ASGI interface.
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

        #ASGITransport = a mock 
        #When the client sends a request, I’ll pass it directly to the ASGI app, just like a real server would—but without leaving memory.
        #AsyncClient = Like requests, but fully async = simulate HTTP calls to API