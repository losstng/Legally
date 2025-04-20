import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.utils.security import create_access_token, create_refresh_token
from app.utils import redis
import time

@pytest.mark.asyncio
async def test_login_and_otp_flow():
    email = "flowtest@example.com"

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
        assert "access_token" in verify_resp.json()["data"]

@pytest.mark.asyncio
async def test_refresh_token_with_access_token_fails():
    token = create_access_token({"email": "flowtest@example.com", "role": "user"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/refresh-token",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid token type."