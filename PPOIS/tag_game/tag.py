# tag.py
import random

class FifteenPuzzle:
    def __init__(self, scramble_on_init=True):
        # создаём упорядоченную доску 4x4 с 0 в правом-нижнем углу
        self.board = [[(i * 4 + j + 1) % 16 for j in range(4)] for i in range(4)]
        if scramble_on_init:
            self.scramble()

    def scramble(self):
        # простая перестановка путём случайных легальных ходов — сохраняет набор чисел
        for _ in range(1000):
            empty_row, empty_col = self.find_empty_pos()
            directions = []
            if empty_col > 0:
                directions.append('left')
            if empty_col < 3:
                directions.append('right')
            if empty_row > 0:
                directions.append('up')
            if empty_row < 3:
                directions.append('down')
            choice = random.choice(directions)
            if choice == 'up':
                # переместить верхнюю плитку вниз (в пустую)
                self.board[empty_row][empty_col], self.board[empty_row-1][empty_col] = \
                    self.board[empty_row-1][empty_col], self.board[empty_row][empty_col]
            elif choice == 'down':
                self.board[empty_row][empty_col], self.board[empty_row+1][empty_col] = \
                    self.board[empty_row+1][empty_col], self.board[empty_row][empty_col]
            elif choice == 'left':
                self.board[empty_row][empty_col], self.board[empty_row][empty_col-1] = \
                    self.board[empty_row][empty_col-1], self.board[empty_row][empty_col]
            elif choice == 'right':
                self.board[empty_row][empty_col], self.board[empty_row][empty_col+1] = \
                    self.board[empty_row][empty_col+1], self.board[empty_row][empty_col]

    def find_empty_pos(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return i, j
        # на всякий случай (не должно случаться) — возвращаем (3,3)
        return 3, 3

    def move(self, row, col):
        # Метод ожидает координаты в формате 1..4 (как в тестах).
        # Возвращает True при успешном ходе, False — если ход невозможен / вход неверен.

        # Проверка типов — тесты ожидают, что при неверном вводе просто вернётся False
        if not isinstance(row, int) or not isinstance(col, int):
            return False

        # Проверка границ в 1..4 (тесты проверяют, что 0 и 5 -> False)
        if row < 1 or row > 4 or col < 1 or col > 4:
            return False

        # Переводим в индексы Python 0..3
        r = row - 1
        c = col - 1

        # Нельзя "перемещать" пустую плитку
        if self.board[r][c] == 0:
            return False

        # Проверяем соседние клетки: если рядом 0 — меняем местами и возвращаем True
        # вверх
        if r > 0 and self.board[r-1][c] == 0:
            self.board[r-1][c], self.board[r][c] = self.board[r][c], 0
            return True
        # вниз
        if r < 3 and self.board[r+1][c] == 0:
            self.board[r+1][c], self.board[r][c] = self.board[r][c], 0
            return True
        # влево
        if c > 0 and self.board[r][c-1] == 0:
            self.board[r][c-1], self.board[r][c] = self.board[r][c], 0
            return True
        # вправо
        if c < 3 and self.board[r][c+1] == 0:
            self.board[r][c+1], self.board[r][c] = self.board[r][c], 0
            return True

        # Никакой соседней пустой клетки — ход невозможен
        return False

    def is_solved(self):
        num = 1
        for i in range(4):
            for j in range(4):
                if i == 3 and j == 3:
                    if self.board[i][j] != 0:
                        return False
                else:
                    if self.board[i][j] != num:
                        return False
                    num += 1
        return True

    def get_item(self, index):
        i, j = index
        return self.board[i][j]

    def __str__(self):
        s = ''
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    s += '   '
                else:
                    s += f'{self.board[i][j]:2d} '
            s += '\n'
        return s


if __name__ == "__main__":
    game = FifteenPuzzle()
    print("Start position: ")
    print(game)

    while not game.is_solved():
        try:
            row = int(input("Enter row (1-4): "))
            col = int(input('Enter col (1-4): '))
            if game.move(row, col):
                print('Move completed: ')
                print(game)
            else:
                print('Not correct move, try again: ')
        except ValueError:
            print('Enter only numbers!')
        except KeyboardInterrupt:
            print('\nGame stopped!')
            break

    if game.is_solved():
        print("Congratulations, you complete the game!")