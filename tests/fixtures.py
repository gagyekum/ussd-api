import json
from ussd_api.session_store import BaseSessionStore

TEST_SESSION_ID = "c6e12905986e4d36b0198978e7f5991e"


class InMemorySessionStore(BaseSessionStore):
    """In-memory session store using a Python dict."""

    def __init__(self):
        self.store = {}

    def get(self, session_id, default=None):
        return self.store.get(session_id, default or {})

    def set(self, session_id, data):
        self.store[session_id] = data


class RedisSessionStore(BaseSessionStore):
    """Redis-based session store for persistent session management."""

    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, session_id, default=None):
        data = self.redis.get(session_id) or default
        return json.loads(data) if isinstance(data, bytes) else data

    def set(self, session_id, data):
        self.redis.set(session_id, json.dumps(data))

    def close(self):
        self.redis.close()


class UnimplementedSessionStore(BaseSessionStore):
    """Session store to demostrate behavior of unimplemented get and set methods"""

    pass
