import json
import os
from ussd_api.consts import (
    INVALID_STATE_MESSAGE,
    MENU_STATE_END,
    INVALID_OPTION_MESSAGE,
    MENU_STATE_START,
)
from ussd_api.exceptions import MenuTemplateFileNotFoundError
from ussd_api.session_store import BaseSessionStore
from ussd_api.state_engine import USSDStateEngine


class USSDMenu:
    """
    Represents a USSD menu item, dynamically setting attributes based on provided parameters.

    This class allows USSD menu parameters to be passed as keyword arguments and sets them as attributes.
    If an attribute is not explicitly defined, it defaults to None.
    """

    def __init__(self, **kwargs):
        """
        Initializes the USSD menu with provided parameters.

        Args:
            kwargs (dict): The keyword arguments representing menu attributes.
        """
        kwargs = {} if kwargs is None else kwargs
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __getattr__(self, name: str):
        """
        Handles missing attributes by returning None instead of raising an AttributeError.

        Args:
            name (str): The requested attribute name.

        Returns:
            None: Default value for undefined attributes.
        """
        return None


class USSDCoreAPI:
    """
    Core engine for handling USSD session processing, including state transitions and menu navigation.

    This class manages session states, processes user inputs, loads USSD menus from a JSON file,
    and provides the ability to navigate forward and backward in the menu flow.

    Attributes:
        session_store (BaseSessionStore): Storage mechanism for session data.
        menu_items (dict): Loaded USSD menu structure from a JSON file.
        state_engine (USSDStateEngine): Manages the session's state transitions.
    """

    def __init__(
        self,
        session_id: str,
        session_store: BaseSessionStore,
        menu_template_path: str,
        initial_state: str | None = None,
    ):
        """
        Initializes the USSD core API with a session store, menu file, and initial state.

        Args:
            session_id (str): Unique identifier for the USSD session.
            session_store (BaseSessionStore): Storage mechanism for session data.
            menu_template_path (str): Path to the JSON file defining USSD menus.
            initial_state (str, optional): The initial state of the session. Defaults to None.
        """
        self.session_store = session_store
        self.menu_items = self._load_menu_from_template(menu_template_path)
        initial_state = initial_state or MENU_STATE_START
        self.state_engine = USSDStateEngine(session_id, initial_state, session_store)

    def _load_menu_from_template(self, menu_template_path: str) -> dict:
        """
        Loads the USSD menu structure from a JSON file.

        The method ensures the correct file path resolution based on the calling application's context.

        Args:
            menu_template_path (str): The path to the JSON menu file.

        Raises:
            RuntimeError: If the file is not found or contains invalid JSON.

        Returns:
            dict: Dictionary representing the USSD menu structure.
        """
        if not os.path.isabs(menu_template_path):
            menu_template_path = os.path.join(os.getcwd(), menu_template_path)

        try:
            with open(menu_template_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise MenuTemplateFileNotFoundError(
                f"Error loading USSD JSON menu file '{menu_template_path}': {e}"
            )

    def process_input(self, user_input: str) -> str:
        """
        Processes user input and determines the next menu response.

        This method checks the current state of the session, validates user input,
        transitions to the next state, and returns the corresponding USSD menu text.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The corresponding USSD menu text, or an error message if the input is invalid.
        """
        current_state = self.state_engine.get_current_state()
        response = INVALID_OPTION_MESSAGE

        if current_state in self.menu_items:
            current_menu = USSDMenu(**self.menu_items[current_state])

            if current_menu.input_required:
                self.state_engine.set_state(current_menu.next_state)
                next_menu = USSDMenu(**self.menu_items[current_menu.next_state])
                response = (next_menu.text or "").replace("${input}", user_input)

            elif user_input in (current_menu.options or {}):
                next_state = current_menu.options[user_input]

                if next_state != MENU_STATE_END:
                    self.state_engine.store_history(current_state)

                self.state_engine.set_state(next_state)
                next_menu = USSDMenu(**self.menu_items[next_state])
                response = next_menu.text

        return response

    def go_back(self) -> str:
        """
        Navigates back to the previous menu state.

        Returns:
            str: The menu text for the previous state, or an error message if unavailable.
        """
        previous_state = self.state_engine.go_back()
        return (self.menu_items.get(previous_state) or {}).get(
            "text"
        ) or INVALID_STATE_MESSAGE
