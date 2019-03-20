import io

from pytest_mock import MockFixture
from unittest.mock import MagicMock


def set_stdin_value(mocker: MockFixture, value: str):
    mocker.patch('builtins.input', return_value=value)


def get_socket_with_mocked_recv(magic_sock: MagicMock, recv_value: bytes):
    magic_sock.return_value.recv.return_value = recv_value

    return magic_sock()
