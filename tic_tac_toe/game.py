from typing import Optional


class WrongMove(Exception):
    pass


class Game:
    def __init__(self, field_size: int, side: str, gamer_name: str, enemy_name: str):
        self.field = []
        self.side = side
        self.field_size = field_size
        self.gamer_name = gamer_name
        self.enemy_name = enemy_name

        for i in range(field_size):
            self.field.append([""] * field_size)

    def move(self, x: int, y: int, side: Optional[str] = None):
        if x >= len(self.field) or x < 0 or y >= len(self.field) or y < 0:
            raise WrongMove("Такой клетки не существует")

        if self.field[x][y] != "":
            raise WrongMove("Эта клетка уже занята")

        self.field[x][y] = side if side else self.side

    def check_winner(self):
        x_winner_line = "X" * len(self.field)
        o_winner_line = "O" * len(self.field)

        for line in range(len(self.field)):
            current_row = "".join(self.field[line])
            current_column = "".join([item[line] for item in self.field])

            if current_row == x_winner_line or current_column == x_winner_line:
                return "X"

            if current_row == o_winner_line or current_column == o_winner_line:
                return "O"

        if (
            "".join([item[i] for i, item in enumerate(self.field)]) == x_winner_line
            or "".join([item[::-1][i] for i, item in enumerate(self.field)]) == x_winner_line
        ):
            return "X"

        if (
            "".join([item[i] for i, item in enumerate(self.field)]) == o_winner_line
            or "".join([item[::-1][i] for i, item in enumerate(self.field)]) == o_winner_line
        ):
            return "O"

        if len([j[i] for j in self.field for i in range(len(self.field)) if j[i] == ""]) == 0:
            return "DRAW"

        return ""

    def draw(self):
        first_line = "  "
        for i in range(len(self.field)):
            first_line += f"| {i + 1} "

        print(first_line)
        for i in range(len(self.field)):
            line = f"{chr(i + 65)} |"
            for j in self.field[i]:
                symb = j if j != "" else " "
                line += f" {symb}  "
            print(line)
