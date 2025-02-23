from fakeredis import FakeRedis
import pytest


@pytest.fixture
def mock_redis_client():
    client = FakeRedis()
    yield client
