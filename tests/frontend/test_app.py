import pytest
import aiohttp


@pytest.fixture
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.mark.asyncio
async def test_health_app(client_session: aiohttp.ClientSession):
    async with client_session.get("http://localhost/assistant") as response:
        status_code = response.status
        assert status_code == 200
