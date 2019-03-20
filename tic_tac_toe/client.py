import argparse
import re
import socket

from tic_tac_toe.exceptions import WrongCommand
from tic_tac_toe.game import Game
from tic_tac_toe.name_generator import get_name

OWN_SIDE = "O"
ENEMY_SIDE = "X"
BUFFER_SIZE = 1024


def init_game(sock: socket.socket, gamer_name: str) -> Game:
    sock.sendall(f"HELO {gamer_name}".encode("utf-8"))

    while True:
        data = sock.recv(BUFFER_SIZE)
        command, *arguments = data.decode("utf-8").split(" ")

        if command == "HELO":
            enemy_name = " ".join([arguments[0], arguments[1]])
            field_size = int(arguments[2].split("x")[0])

            return Game(field_size, OWN_SIDE, gamer_name, enemy_name)
        else:
            raise WrongCommand


def make_step(sock: socket.socket, game: Game):
    def make_move():
        cell = input("Ваш ход: ")
        while not re.match(r"[A-Z] \d", cell) or ord(cell.split(" ")[0]) - 65 >= game.field_size:
            print(
                "Введите клетку в формате: Буква Цифра. Клетка не должна выходить за пределы игрового поля."
            )
            cell = input("Ваш ход: ")
        own_x, own_y = cell.split(" ")
        is_move_sucсess = False
        while not is_move_sucсess:
            try:
                game.move(ord(own_x) - 65, int(own_y) - 1)
                sock.sendall(f"MOVE {cell}".encode("utf-8"))
            except Exception as e:
                print(is_move_sucсess)
                print(e)
                make_move()

            is_move_sucсess = True
            print(is_move_sucсess)

            print("MEOW")

    game_over = False
    print(f"Ожидание хода игрока {game.enemy_name}")

    data = sock.recv(BUFFER_SIZE)
    command, *arguments = data.decode("utf-8").split(" ")

    if command == "MOVE":
        enemy_x, enemy_y, *rest = arguments
        try:
            print(enemy_x, enemy_y)
            game.move(ord(enemy_x) - 65, int(enemy_y) - 1, ENEMY_SIDE)
        except Exception as e:
            print(e)

        if rest:
            game_over = True
            winner = rest[1]
            game.draw()

            if winner == "DRAW":
                print("Результат игры - ничья")
            else:
                print(f"Выиграл игрок {game.gamer_name if winner == OWN_SIDE else game.enemy_name}")

            return game_over
    elif command == "STOP":
        game_over = True
        winner = arguments[0]

        if winner == "DRAW":
            print("Результат игры - ничья")
        else:
            print(f"Выиграл игрок {game.gamer_name if winner == OWN_SIDE else game.enemy_name}")

        return game_over
    else:
        raise WrongCommand

    game.draw()

    make_move()
    game.draw()

    return game_over


def main():
    parser = argparse.ArgumentParser(description="tic_tac_toe client")
    parser.add_argument("host", help="host")
    parser.add_argument("port", help="port", type=int)
    args = parser.parse_args()

    with socket.socket() as sock:
        sock.connect((args.host, args.port))

        gamer_name = get_name()
        print(f"Привет, игрок {gamer_name}")

        game = init_game(sock, gamer_name)
        print(f"К вам присоединился игрок {game.enemy_name}")
        print(f"Размер поля - {game.field_size}x{game.field_size}")

        game.draw()

        while True:
            game_over = make_step(sock, game)

            if game_over:
                break


if __name__ == "__main__":
    main()
