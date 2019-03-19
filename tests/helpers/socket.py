from unittest.mock import MagicMock


def get_socket_with_mocked_recv(magic_sock: MagicMock, recv_value: bytes):
    magic_sock.return_value.recv.return_value = recv_value

    return magic_sock()
