import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import get_db
from app.db import models
from app.utils.security import hash_password, create_access_token, create_refresh_token
from app.utils import redis
from fastapi import HTTPException
import time

#@pytest.mark.asyncio
#async def test_register_user():
#    transport = ASGITransport(app=app)
#    async with AsyncClient(transport=transport, base_url="http://test") as ac:
#        response = await ac.post("/auth/register", json={
#            "name": "Test User",
#           "age": 30,
#          "email": "long131005@outlook.com",
#            "password": "strongpassword"
#        })
#        print("STATUS:", response.status_code)
#    print("RESPONSE:", response.json())
#    assert response.status_code == 200
#    assert "access_token" in response.json()



@pytest.mark.asyncio
async def test_register_duplicate_email():
    db = next(get_db())
    user = models.User(
        name="Already Exists",
        age=30,
        email="long131005@outlook.com",
        hashed_password=hash_password("abc"),
        role="user"
    )

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not existing_user:
        db.add(user)
        db.commit()
        db.refresh(user)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "name": "Test Dupe",
            "age": 22,
            "email": "dupe@example.com",
            "password": "whatever"
        })
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_and_otp_flow():
    email = "flowtest@example.com"
    db = next(get_db())

    # Make sure user exists
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            name="Login Flow",
            age=25,
            email=email,
            hashed_password=hash_password("pass123"),
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Step 1: Login
        login_resp = await ac.post("/auth/login", json={"email": email, "password": "pass123"})
        assert login_resp.status_code == 200

        # Step 2: Wait for OTP to be set
        time.sleep(1)
        otp = redis.redis_client.get(f"otp:{email}")
        otp = otp.decode() if hasattr(otp, "decode") else otp
        assert otp is not None

        # Step 3: Verify OTP
        verify_resp = await ac.post("/auth/verify-otp", json={"email": email, "otp": otp})
        print("STATUS:", verify_resp.status_code)
        print("RESPONSE:", verify_resp.json())

        assert verify_resp.status_code == 200
        assert "access_token" in verify_resp.json()

@pytest.mark.asyncio
async def test_refresh_token_success():
    # Simulate a valid refresh token for a user
    token = create_refresh_token({"email": "flowtest@example.com", "role": "user"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/refresh-token",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_refresh_token_with_access_token_fails():
    # Generate a regular access token instead of refresh
    token = create_access_token({"email": "flowtest@example.com", "role": "user"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/refresh-token",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid token type."