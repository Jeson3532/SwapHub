import pytest
import aiohttp


@pytest.fixture
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.mark.asyncio
async def test_ip_check(client_session: aiohttp.ClientSession):
    async with client_session.get("http://localhost/check-ip") as response:
        status_code = response.status
        assert status_code == 200

        result = await response.json()
        assert result

        keys = result.keys()
        assert 'client_host' in keys
        assert 'x_forwarded_for' in keys
        assert 'x_real_ip' in keys
