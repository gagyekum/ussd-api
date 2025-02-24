from ussd_api.session_store import BaseSessionStore


class USSDStateEngine:
    """
    Manages the state transitions for a USSD session.

    This class maintains the current state of a USSD session, supports state transitions,
    stores navigation history, and allows users to go back to a previous state.

    Attributes:
        session_id (str): Unique identifier for the USSD session.
        initial_state (str): The starting state for the session.
        session_store (BaseSessionStore): Storage mechanism for session data.
    """

    def __init__(
        self, session_id: str, initial_state: str, session_store: BaseSessionStore
    ) -> None:
        """
        Initializes the USSD state engine.

        Args:
            session_id (str): The unique identifier for the session.
            initial_state (str): The initial state of the USSD session.
            session_store (BaseSessionStore): The session store instance for managing session data.
        """
        self.session_id = session_id
        self.initial_state = initial_state
        self.session_store = session_store

    def get_current_state(self) -> str:
        """
        Retrieves the current state of the USSD session.

        Returns:
            str: The current state of the session. If no state is found in the session store,
                 the initial state is returned.
        """
        return (self.session_store.get(self.session_id) or {}).get(
            "state"
        ) or self.initial_state

    def set_state(self, state: str) -> None:
        """
        Updates the session state to a new state.

        Args:
            state (str): The new state to transition to.
        """
        session_data = self.session_store.get(self.session_id) or {}
        session_data["state"] = state
        self.session_store.set(self.session_id, session_data)

    def store_history(self, state: str) -> None:
        """
        Stores the current state in session history to enable navigation back.

        Args:
            state (str): The state to be stored in history.
        """
        session_data = self.session_store.get(self.session_id) or {}
        history = session_data.get("history") or []
        history.append(state)
        session_data["history"] = history
        self.session_store.set(self.session_id, session_data)

    def go_back(self) -> str:
        """
        Navigates back to the previous state in the session history.

        Returns:
            str: The previous state if available, otherwise returns the initial state.
        """
        session_data = self.session_store.get(self.session_id) or {}
        history = session_data.get("history") or []
        if history:
            history.pop()
            session_data["state"] = history[-1] if history else self.initial_state
            session_data["history"] = history
            self.session_store.set(self.session_id, session_data)
        return session_data.get("state") or self.initial_state
