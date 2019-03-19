import pytest
from pytest_mock import MockFixture

from tic_tac_toe.exceptions import WrongCommand
from tic_tac_toe.server import init_game, make_step
from tests.helpers.input import set_stdin_value
from tests.helpers.socket import get_socket_with_mocked_recv


def test_game_initializes(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO boring Hawking".encode("utf-8"))

        try:
            init_game(sock, 3, "happy Pascal")
        except WrongCommand:
            pytest.fail()
        finally:
            sock.close()


def test_game_starts_incorrectly(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HEY! boring Hawking".encode("utf-8"))

        with pytest.raises(WrongCommand):
            init_game(sock, 3, "happy Pascal")
            sock.close()


def test_enemy_send_wrong_command(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO boring Hawking".encode("utf-8"))
        game = init_game(sock, 3, "happy Pascal")

        set_stdin_value(mocker, "A 2")
        sock = get_socket_with_mocked_recv(mock_socket_cls, "WRONG_MOVE A 1".encode("utf-8"))

        with pytest.raises(WrongCommand):
            make_step(sock, game)


def test_game_correctly_ends(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO boring Hawking".encode("utf-8"))
        game = init_game(sock, 1, "happy Pascal")

        sendall_spy = mocker.spy(sock, "sendall")
        set_stdin_value(mocker, "A 1")
        make_step(sock, game)
        sock.close()

        assert game.check_winner() == "X"
        sendall_spy.assert_called_once_with("MOVE A 1 STOP X".encode("utf-8"))


def test_game_continues_after_step(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO boring Hawking".encode("utf-8"))
        game = init_game(sock, 2, "happy Pascal")
        sock.close()

        set_stdin_value(mocker, "A 1")
        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE B 1".encode("utf-8"))
        game_over = make_step(sock, game)
        sock.close()

        assert not game_over

        set_stdin_value(mocker, "A 2")
        sock = mock_socket_cls()
        sendall_spy = mocker.spy(sock, "sendall")
        game_over = make_step(sock, game)
        sock.close()

        assert game_over
        sendall_spy.assert_called_once_with("MOVE A 2 STOP X".encode("utf-8"))


def test_enemy_wins(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO boring Hawking".encode("utf-8"))
        game = init_game(sock, 3, "happy Pascal")

        set_stdin_value(mocker, "A 2")
        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE A 1".encode("utf-8"))
        make_step(sock, game)

        set_stdin_value(mocker, "B 1")
        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE B 2".encode("utf-8"))
        make_step(sock, game)

        set_stdin_value(mocker, "C 2")
        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE C 3".encode("utf-8"))
        sendall_spy = mocker.spy(sock, "sendall")
        make_step(sock, game)

        sendall_spy.assert_called_with("STOP O".encode("utf-8"))
