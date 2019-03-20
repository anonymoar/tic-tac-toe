from typing import Optional


class WrongMove(Exception):
    pass


X_SIDE = "X"
Y_SIDE = "O"
DRAW = "DRAW"


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
        if x >= self.field_size or x < 0 or y >= self.field_size or y < 0:
            raise WrongMove("Такой клетки не существует")

        if self.field[x][y] != "":
            raise WrongMove("Эта клетка уже занята")

        self.field[x][y] = side if side else self.side

    def check_is_winner(self, side):
        winner_line = side * self.field_size

        for line in range(self.field_size):
            current_row = "".join(self.field[line])
            current_column = "".join([item[line] for item in self.field])

            if current_row == winner_line or current_column == winner_line:
                return side

        if (
            "".join([item[i] for i, item in enumerate(self.field)]) == winner_line
            or "".join([item[::-1][i] for i, item in enumerate(self.field)]) == winner_line
        ):
            return side

        return None

    def check_winner(self):
        if self.check_is_winner(X_SIDE):
            return X_SIDE
        elif self.check_is_winner(Y_SIDE):
            return Y_SIDE

        if len([j[i] for j in self.field for i in range(self.field_size) if j[i] == ""]) == 0:
            return DRAW

        return None

    def draw(self):
        first_line = "  "
        for i, _ in enumerate(self.field):
            first_line += f"| {i + 1} "

        print(first_line)
        for i in range(self.field_size):
            line = f"{chr(i + 65)} |"
            for j in self.field[i]:
                symb = j or " "
                line += f" {symb}  "
            print(line)
