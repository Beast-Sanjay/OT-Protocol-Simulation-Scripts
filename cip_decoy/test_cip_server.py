import pytest
from unittest.mock import patch, MagicMock
import socket
from unittest.mock import MagicMock
from pytest_mock import mocker

from cip_server import cipServer


@pytest.fixture
def cip_class():
    return cipServer()

def test_get_ip_address_success(cip_class):

    # Mock socket methods to simulate a successful IP address retrieval
    with patch('socket.socket') as mock_socket:
        mock_instance = mock_socket.return_value
        mock_instance.getsockname.return_value = ('192.168.100.3', 0)

        ip_address = cip_class.get_ip_address()

        assert ip_address == '192.168.100.3'
        mock_instance.connect.assert_called_with(("8.8.8.8", 80))
        mock_instance.close.assert_called_once()

def test_get_ip_address_socket_error(cip_class):

    # Mock socket methods to simulate a socket error
    with patch('socket.socket') as mock_socket:
        mock_instance = mock_socket.return_value
        mock_instance.connect.side_effect = socket.error

        ip_address = cip_class.get_ip_address()

        assert ip_address == "Unable to get IP Address"
        mock_instance.connect.assert_called_with(("8.8.8.8", 80))

def test_send_response_valid_request(cip_class):
    cip_class.gramophile_dict = {
        "010203": "040506"
    }
    response = cip_class.send_response("01 02 03")
    assert response == b'\x04\x05\x06'

def test_send_response_invalid_request(cip_class):
    cip_class.gramophile_dict = {
        "010203": "040506"
    }
    response = cip_class.send_response("FF EE DD")
    assert response == ""

def test_send_response_non_hex_input(cip_class):
    cip_class.gramophile_dict = {
        "010203": "040506"
    }
    response = cip_class.send_response("G1 H2 I3")
    assert response == ""
    


# def test_socket_connection():
#     server = cipServer()

#     with patch('socket.socket') as mock_socket:
#         mock_socket_instance = MagicMock()
#         mock_socket.return_value = mock_socket_instance

#         # Mock methods of the socket instance
#         mock_socket_instance.accept.return_value = (MagicMock(), ('127.0.0.1', 12345))
#         mock_socket_instance.recv.return_value = b"test data"

#         # Mock send_response method
#         server.send_response = MagicMock(return_value=b"Response: test data")

#         # Run the socket_connection method (break the infinite loop after first iteration)
#         with patch.object(server, 'socket_connection', wraps=server.socket_connection) as mock_method:
#             try:
#                 server.socket_connection()
#             except KeyboardInterrupt:
#                 pass  # This is just to stop the infinite loop after the test

#             mock_socket_instance.bind.assert_called_with(('localhost', 8080))
#             mock_socket_instance.listen.assert_called_once()
#             mock_socket_instance.accept.assert_called_once()
#             mock_socket_instance.recv.assert_called_once_with(4096)
#             server.send_response.assert_called_once()
#             mock_socket_instance.sendall.assert_called_once_with(b"Response: test data")


if __name__ == "__main__":
    pytest.main()