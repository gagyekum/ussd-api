import json
import pytest

from tests.fixtures import (
    TEST_SESSION_ID,
    InMemorySessionStore,
    RedisSessionStore,
    UnimplementedSessionStore,
)


def test_in_memory_session_store_saves_and_retrieves_data_successfully():
    data = {"field": "value"}

    store = InMemorySessionStore()
    store.set(TEST_SESSION_ID, data)

    assert store.get(TEST_SESSION_ID) == data


@pytest.mark.parametrize(
    "default,expected_result", [(None, {}), ("No data", "No data"), (0, {})]
)
def test_in_memory_session_store_return_specified_default_if_no_data(
    default, expected_result
):
    store = InMemorySessionStore()

    assert store.get(TEST_SESSION_ID, default) == expected_result


def test_redis_session_store_saves_and_retrieves_data_successfully(
    mocker, mock_redis_client
):
    data = {"field": "value"}
    jsonified_data = json.dumps(data)

    with RedisSessionStore(mock_redis_client) as store:
        mocker.patch.object(store, "close")
        store.set(TEST_SESSION_ID, jsonified_data)

        assert mock_redis_client.exists(TEST_SESSION_ID)
        assert json.loads(store.get(TEST_SESSION_ID)) == data

    store.close.assert_called_once()


@pytest.mark.parametrize(
    "default,expected_result", [(None, None), ("No data", "No data"), (0, 0)]
)
def test_redis_session_store_returns_default_value_if_no_data_is_found(
    mocker, mock_redis_client, default, expected_result
):
    with RedisSessionStore(mock_redis_client) as store:
        mocker.patch.object(store, "close")

        assert mock_redis_client.exists(TEST_SESSION_ID) == 0
        assert store.get(TEST_SESSION_ID, default) == expected_result

    store.close.assert_called_once()


def test_unimplemented_session_store_fails():
    with pytest.raises(TypeError):
        UnimplementedSessionStore()
