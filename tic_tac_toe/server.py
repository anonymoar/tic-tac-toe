import argparse
import re
import socket
import sys

from tic_tac_toe.exceptions import WrongCommand
from tic_tac_toe.game import Game
from tic_tac_toe.name_generator import get_name

OWN_SIDE = "X"
ENEMY_SIDE = "O"
BUFFER_SIZE = 1024
CLIENTS_MAX_COUNT = 1


def init_game(sock: socket.socket, field_size: int, gamer_name: str) -> Game:
    while True:
        data = sock.recv(BUFFER_SIZE)
        command, *arguments = data.decode("utf-8").split(" ")

        if command == "HELO":
            enemy_name = " ".join(arguments)
            sock.sendall(f"HELO {gamer_name} {field_size}x{field_size}".encode("utf-8"))

            return Game(field_size, OWN_SIDE, gamer_name, enemy_name)
        else:
            raise WrongCommand


def make_step(sock: socket.socket, game: Game):
    game_over = False

    def make_move(is_move_success):
        cell = input("Ваш ход: ")
        while not re.match(r"^[A-Z] \d$", cell) or ord(cell.split(" ")[0]) - 65 >= game.field_size:
            print(
                "Введите клетку в формате: Буква Цифра. Клетка не должна выходить за пределы игрового поля."
            )
            cell = input("Ваш ход: ")
        own_x, own_y = cell.split(" ")
        while not is_move_success:
            try:
                print(cell)
                game.move(ord(own_x) - 65, int(own_y) - 1)
            except Exception as e:
                print(e)
                cell = make_move(is_move_success)
            is_move_success = True

        print(cell)
        return cell

    cell = make_move(False)
    print(cell)
    game.draw()
    winner = game.check_winner()

    if winner:
        game_over = True
        if winner == "DRAW":
            print("Результат игры - ничья")
        else:
            print(f"Выиграл игрок {game.gamer_name if winner == OWN_SIDE else game.enemy_name}")

        sock.sendall(f"MOVE {cell} STOP {winner}".encode("utf-8"))
        sock.close()

        return game_over
    else:
        print(cell)
        sock.sendall(f"MOVE {cell}".encode("utf-8"))

    print(f"Ожидание хода игрока {game.enemy_name}")

    data = sock.recv(BUFFER_SIZE)
    command, *arguments = data.decode("utf-8").split(" ")

    if command == "MOVE":
        enemy_x, enemy_y = arguments
        try:
            game.move(ord(enemy_x) - 65, int(enemy_y) - 1, ENEMY_SIDE)
        except Exception as e:
            print(e)
    else:
        print("Неверная команда")

    winner = game.check_winner()
    game.draw()

    if winner:
        sock.sendall(f"STOP {winner}".encode("utf-8"))
        if winner == "DRAW":
            print("Результат игры - ничья")
        else:
            print(f"Выиграл игрок {game.gamer_name if winner == OWN_SIDE else game.enemy_name}")
        game_over = True
        sock.close()

    return game_over


def main():
    parser = argparse.ArgumentParser(description="tic_tac_toe server")
    parser.add_argument("host", help="host")
    parser.add_argument("port", help="port", type=int)
    parser.add_argument("size", help="field size")
    args = parser.parse_args()

    if int(args.size.split("x")[0]) != int(args.size.split("x")[1]):
        print("Неправильно указан размер поля игры. Оно должно быть квадратным.")
        return

    with socket.socket() as sock:
        try:
            sock.bind((args.host, args.port))
            sock.listen(CLIENTS_MAX_COUNT)

            print(f"Ожидание подключения противника")
            conn, addr = sock.accept()

            gamer_name = get_name()
            print(f"Привет, игрок {gamer_name}")

            field_size = int(args.size.split("x")[0])

            game = init_game(conn, field_size, gamer_name)
            print(f"К вам присоединился игрок {game.enemy_name}")

            game.draw()

            while True:
                game_over = make_step(conn, game)

                if game_over:
                    break
        except WrongCommand:
            print("Клиент передал некорректную команду", file=sys.stderr)
            # make_step(conn, game)
            sock.close()
        except OSError as e:
            print(e, file=sys.stderr)
            sock.close()


if __name__ == "__main__":
    main()
