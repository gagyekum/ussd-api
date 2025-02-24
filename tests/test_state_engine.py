from ussd_api.consts import MENU_STATE_START


def test_ussd_state_engine_initial_state(mock_state_engine):
    assert mock_state_engine.get_current_state() == MENU_STATE_START


def test_ussd_state_engine_set_state(mock_state_engine):
    mock_state_engine.set_state("next_state")
    assert mock_state_engine.get_current_state() == "next_state"


def test_ussd_state_engine_store_and_go_back(mock_state_engine):
    mock_state_engine.set_state("menu_1")
    mock_state_engine.store_history("menu_1")
    mock_state_engine.set_state("menu_2")
    mock_state_engine.store_history("menu_2")

    assert mock_state_engine.go_back() == "menu_1"
    assert mock_state_engine.go_back() == MENU_STATE_START
    assert mock_state_engine.go_back() == MENU_STATE_START
