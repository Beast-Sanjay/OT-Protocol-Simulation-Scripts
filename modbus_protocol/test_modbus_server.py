import pytest
from unittest.mock import patch, Mock
import socket
from unittest.mock import MagicMock
from pytest_mock import mocker

from modbus_server import ModbusServer


@pytest.fixture
def modbus_class():
    return ModbusServer()

def test_get_ip_address_success(modbus_class):

    # Mock socket methods to simulate a successful IP address retrieval
    with patch('socket.socket') as mock_socket:
        mock_instance = mock_socket.return_value
        mock_instance.getsockname.return_value = ('192.168.100.3', 0)

        ip_address = modbus_class.get_ip_address()

        assert ip_address == '192.168.100.3'
        mock_instance.connect.assert_called_with(("8.8.8.8", 80))
        mock_instance.close.assert_called_once()

def test_get_ip_address_socket_error(modbus_class):

    # Mock socket methods to simulate a socket error
    with patch('socket.socket') as mock_socket:
        mock_instance = mock_socket.return_value
        mock_instance.connect.side_effect = socket.error

        ip_address = modbus_class.get_ip_address()

        assert ip_address == "Unable to get IP Address"
        mock_instance.connect.assert_called_with(("8.8.8.8", 80))

def test_send_response_valid_request(modbus_class):
    modbus_class.gramophile_dict = {
        "010203": "040506"
    }
    response = modbus_class.send_response("01 02 03")
    assert response == b'\x04\x05\x06'

def test_send_response_invalid_request(modbus_class):
    modbus_class.gramophile_dict = {
        "010203": "040506"
    }
    response = modbus_class.send_response("FF EE DD")
    assert response == ""

def test_send_response_non_hex_input(modbus_class):
    modbus_class = ModbusServer()
    modbus_class.gramophile_dict = {
        "010203": "040506"
    }
    response = modbus_class.send_response("G1 H2 I3")
    assert response == ""
    


def test_socket_connection_success(mocker, modbus_class):
    mock_socket = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket.return_value.__enter__.return_value
    mock_socket_instance.accept.return_value = (MagicMock(), ('193.168.100.3', 502))
    mock_socket_instance.recv.return_value = b"test_payload"

    # Mock the send_response method
    mocker.patch.object(modbus_class, 'send_response', return_value=b"response_payload")

    result = modbus_class.socket_connection()

    assert result is True
    

if __name__ == "__main__":
    pytest.main()