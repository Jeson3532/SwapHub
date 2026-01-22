import pytest
import aiohttp
from src.backend.auth.oauth import create_access_token


@pytest.fixture
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture()
def test_token():
    payload = {
        'identifier': 'testing',
        'display_name': 'testing',
        'metadata': {}
    }
    return create_access_token(**payload, time_minutes=3)


@pytest.mark.asyncio
async def test_ip_check(client_session: aiohttp.ClientSession, test_token):
    cookies = {'access_token': test_token}
    async with client_session.get("http://localhost/check-my-ip", cookies=cookies) as response:
        status_code = response.status
        assert status_code == 200

        result = await response.json()
        assert result

        keys = result.keys()
        assert 'client_host' in keys
        assert 'x_forwarded_for' in keys
        assert 'x_real_ip' in keys
