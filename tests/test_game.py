import pytest
from tic_tac_toe.game import Game, WrongMove


def test_init_game():
    game = Game(2, "X", "MEOW", "KOTIK")
    assert len(game.field) == 2
    assert game.field == [["", ""], ["", ""]]
    assert game.side == "X"
    assert game.gamer_name == "MEOW"
    assert game.enemy_name == "KOTIK"


def test_move_success():
    game = Game(2, "X", "MEOW", "KOTIK")
    game.move(1, 1)
    assert game.field[1][1] == game.side


@pytest.mark.parametrize(
    "moves, error_message",
    [
        ((3, 3), "Такой клетки не существует"),
        ((-1, 4), "Такой клетки не существует"),
        ((-1, -2), "Такой клетки не существует"),
        ((-1, 1), "Такой клетки не существует"),
    ],
)
def test_move_raises_wrong_move_exception_cell_not_found(moves, error_message):
    game = Game(2, "X", "MEOW", "KOTIK")
    with pytest.raises(WrongMove) as excinfo:
        x, y = moves
        game.move(x, y)
    assert "Такой клетки не существует" in str(excinfo.value)


def test_move_raises_wrong_move_exception_cell_already_taken():
    game = Game(2, "X", "MEOW", "KOTIK")
    game.move(1, 1)
    with pytest.raises(WrongMove) as excinfo:
        game.move(1, 1)
    assert "Эта клетка уже занята" in str(excinfo.value)


@pytest.mark.parametrize(
    "moves, winner_expected",
    [
        (
            [
                (0, 0, "X"),
                (0, 1, "O"),
                (0, 2, "X"),
                (1, 0, "X"),
                (1, 1, "O"),
                (1, 2, "X"),
                (2, 0, "O"),
                (2, 1, "X"),
                (2, 2, "O"),
            ],
            "DRAW",
        ),
        ([(0, 0, "X"), (0, 1, "O"), (0, 2, "X"), (2, 1, "X"), (2, 2, "O")], None),
        ([(0, 0, "X"), (0, 1, "X"), (0, 2, "X")], "X"),
        ([(1, 0, "X"), (1, 1, "X"), (1, 2, "X")], "X"),
        ([(2, 0, "X"), (2, 1, "X"), (2, 2, "X")], "X"),
        ([(0, 0, "O"), (0, 1, "O"), (0, 2, "O")], "O"),
        ([(1, 0, "O"), (1, 1, "O"), (1, 2, "O")], "O"),
        ([(2, 0, "O"), (2, 1, "O"), (2, 2, "O")], "O"),
        ([(0, 0, "X"), (1, 0, "X"), (2, 0, "X")], "X"),
        ([(0, 1, "X"), (1, 1, "X"), (2, 1, "X")], "X"),
        ([(0, 2, "X"), (1, 2, "X"), (2, 2, "X")], "X"),
        ([(0, 0, "O"), (1, 0, "O"), (2, 0, "O")], "O"),
        ([(0, 1, "O"), (1, 1, "O"), (2, 1, "O")], "O"),
        ([(0, 2, "O"), (1, 2, "O"), (2, 2, "O")], "O"),
        ([(0, 0, "X"), (1, 1, "X"), (2, 2, "X")], "X"),
        ([(0, 2, "X"), (1, 1, "X"), (2, 0, "X")], "X"),
        ([(0, 0, "O"), (1, 1, "O"), (2, 2, "O")], "O"),
        ([(0, 2, "O"), (1, 1, "O"), (2, 0, "O")], "O"),
    ],
)
def test_check_winner_draw_or_no_yet_winner(moves, winner_expected):
    game = Game(3, "X", "MEOW", "KOTIK")
    for i in moves:
        x, y, z = i
        game.move(x, y, z)
    assert game.check_winner() == winner_expected


def test_draw(capsys):
    game = Game(4, "X", "MEOW", "KOTIK")
    game.move(0, 0, "X")
    game.move(0, 2, "O")
    game.move(1, 0, "O")
    game.move(1, 1, "X")
    game.move(2, 2, "O")
    assert (
        game.draw()
        == "  | 1 | 2 | 3 | 4 \nA | X       O      \nB | O   X          \nC |         O      \nD |                \n"
    )
