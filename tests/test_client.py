import pytest
from pytest_mock import MockFixture

from tic_tac_toe.exceptions import WrongCommand
from tic_tac_toe.client import init_game, make_step
from tests.helpers.input import set_stdin_value
from tests.helpers.socket import get_socket_with_mocked_recv


def test_game_initializes(mocker: MockFixture):
    mock_socket_cls = mocker.patch("socket.socket")
    sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO happy Pascal 3x3".encode("utf-8"))

    try:
        game = init_game(sock, "boring Hawking")
    except WrongCommand:
        pytest.fail()
        return

    assert game.field_size == 3
    assert game.enemy_name == "happy Pascal"


def test_game_starts_incorrectly(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "OMG happy Pascal 3x3".encode("utf-8"))

        with pytest.raises(WrongCommand):
            init_game(sock, "boring Hawking")

        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO happy Pascal ??".encode("utf-8"))

        with pytest.raises(ValueError):
            init_game(sock, "boring Hawking")


def test_enemy_send_wrong_command(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO happy Pascal 1x1".encode("utf-8"))
        game = init_game(sock, "boring Hawking")

        sock = get_socket_with_mocked_recv(mock_socket_cls, "OMG A 1".encode("utf-8"))

        with pytest.raises(WrongCommand):
            make_step(sock, game)


def test_game_correctly_ends(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO happy Pascal 1x1".encode("utf-8"))
        game = init_game(sock, "boring Hawking")

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE A 1 STOP X".encode("utf-8"))
        game_over = make_step(sock, game)
        sock.close()

        assert game_over
        assert game.check_winner() == "X"


def test_enemy_wins(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO happy Pascal 3x3".encode("utf-8"))
        game = init_game(sock, "boring Hawking")

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE A 1".encode("utf-8"))
        set_stdin_value(mocker, "A 2")
        make_step(sock, game)

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE B 2".encode("utf-8"))
        set_stdin_value(mocker, "B 1")
        make_step(sock, game)

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE C 3 STOP X".encode("utf-8"))
        game_over = make_step(sock, game)

        assert game_over
        assert game.check_winner() == "X"


def test_gamer_wins(mocker: MockFixture):
    with mocker.patch("socket.socket") as mock_socket_cls:
        sock = get_socket_with_mocked_recv(mock_socket_cls, "HELO happy Pascal 3x3".encode("utf-8"))
        game = init_game(sock, "boring Hawking")

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE A 2".encode("utf-8"))
        set_stdin_value(mocker, "A 1")
        make_step(sock, game)

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE B 1".encode("utf-8"))
        set_stdin_value(mocker, "B 2")
        make_step(sock, game)

        sock = get_socket_with_mocked_recv(mock_socket_cls, "MOVE C 2".encode("utf-8"))
        set_stdin_value(mocker, "C 3")
        make_step(sock, game)

        sock = get_socket_with_mocked_recv(mock_socket_cls, "STOP O".encode("utf-8"))
        game_over = make_step(sock, game)

        assert game_over
        assert game.check_winner() == "O"
