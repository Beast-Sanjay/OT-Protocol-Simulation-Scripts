import pytest
from unittest.mock import patch, Mock
import socket
from unittest.mock import MagicMock
from pytest_mock import mocker

from bacnet_server import bacnet_server


@pytest.fixture
def bacnet_class():
    return bacnet_server()

def test_get_ip_address(bacnet_class):
    # Mock the socket module and set the return value of gethostname() to a dummy hostname
    with patch('socket.gethostname', return_value='dummy_hostname'):
        # Call the get_ip_address() method
        ip_address = bacnet_class.get_ip_address()
        
        # Assert that the ip_address is a string
        assert isinstance(ip_address, str)
        
        # Assert that the ip_address is not empty
        assert ip_address != ''

def test_udp_socket_connection(bacnet_class):
    # Mock the socket module and create a mock socket object
    mock_socket = MagicMock()
    mock_socket.recvfrom.return_value = (b'dummy_data', ('dummy_address', 1234))
    with patch('socket.socket', return_value=mock_socket):
        # Call the udp_socket_connection() method
        bacnet_class.udp_socket_connection()
        
        # Assert that the socket.recvfrom() method is called once
        mock_socket.recvfrom.assert_called_once()