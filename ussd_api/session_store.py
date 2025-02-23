from abc import ABC, abstractmethod


class BaseSessionStore(ABC):
    """Abstract base class for session storage."""

    @abstractmethod
    def get(self, session_id, default=None):
        """Retrieve session data by session_id.

        Args:
            session_id: Session ID
            default: Default value if not data is returned. Defaults to None.
        """
        pass

    @abstractmethod
    def set(self, session_id, data):
        """Store session data by session_id.

        Args:
            session_id: Session ID
            data: Data to store in session
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close any open resources."""
        pass
