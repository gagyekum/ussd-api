from fakeredis import FakeRedis
import pytest

from tests.fixtures import TEST_SESSION_ID, InMemorySessionStore, RedisSessionStore
from ussd_api.consts import MENU_STATE_START
from ussd_api.core import USSDCoreAPI
from ussd_api.state_engine import USSDStateEngine


@pytest.fixture
def mock_redis_client():
    return FakeRedis()


@pytest.fixture
def mock_in_memory_session_store():
    return InMemorySessionStore()


@pytest.fixture
def mock_redis_session_store(mock_redis_client):
    return RedisSessionStore(mock_redis_client)


@pytest.fixture
def mock_state_engine(mock_redis_session_store):
    return USSDStateEngine(
        session_id=TEST_SESSION_ID,
        initial_state=MENU_STATE_START,
        session_store=mock_redis_session_store,
    )


@pytest.fixture
def mock_ussd_core_api(mock_redis_session_store):
    """Provides an instance of USSDCoreAPI with a mock menu."""
    with mock_redis_session_store:
        yield USSDCoreAPI(
            session_id=TEST_SESSION_ID,
            session_store=mock_redis_session_store,
            menu_template_path="tests/menu-template.json",
        )
