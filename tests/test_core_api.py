from ussd_api.consts import INVALID_OPTION_MESSAGE, MENU_STATE_START
from ussd_api.core import USSDMenu


def test_ussd_menu_dynamic_attributes():
    menu = USSDMenu(title="Main Menu", text="Welcome!", next_state="next")

    assert menu.title == "Main Menu"
    assert menu.text == "Welcome!"
    assert menu.next_state == "next"


def test_ussd_menu_missing_attributes():
    menu = USSDMenu()

    assert menu.some_non_existent_attribute is None


def test_ussd_core_load_menu(mock_ussd_core_api):
    assert MENU_STATE_START in mock_ussd_core_api.menu_items
    assert (
        mock_ussd_core_api.menu_items[MENU_STATE_START]["text"]
        == "Welcome to USSD App\n1. Balance\n2. Buy Airtime\n3. Exit"
    )


def test_ussd_core_process_valid_input(mock_ussd_core_api):
    response = mock_ussd_core_api.process_input("1")

    assert response == "Your balance is $10.\n0. Back"


def test_ussd_core_process_invalid_input(mock_ussd_core_api):
    response = mock_ussd_core_api.process_input("9")

    assert response == INVALID_OPTION_MESSAGE


def test_ussd_core_go_back(mock_ussd_core_api):
    mock_ussd_core_api.process_input("1")

    assert (
        mock_ussd_core_api.go_back()
        == "Welcome to USSD App\n1. Balance\n2. Buy Airtime\n3. Exit"
    )


def test_ussd_core_process_input_required(mock_ussd_core_api):
    response = mock_ussd_core_api.process_input("2")
    assert response == "Enter amount to buy airtime:"

    user_input = "10"
    response = mock_ussd_core_api.process_input(user_input)
    assert response == f"Confirm purchase of {user_input} airtime?\n1. Yes\n2. No"


def test_ussd_core_process_exit(mocker, mock_ussd_core_api):
    response = mock_ussd_core_api.process_input("3")
    mock_store_history = mocker.patch.object(
        mock_ussd_core_api.state_engine, "store_history"
    )

    assert response == "Thank you for using our service."
    mock_store_history.assert_not_called()
