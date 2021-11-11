from main import return_state


def test_bluetooth_state():
    # Arrange
    addr = "F4:AF:E7:72:CB:19"

    # Act
    state = return_state(addr)

    # Assert
    assert state is None
