import unittest
import sys
import io
from unittest.mock import patch
from tag import FifteenPuzzle

class TestFifteenPuzzle(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации игры"""
        game = FifteenPuzzle()
        
        # Проверяем размер доски
        self.assertEqual(len(game.board), 4)
        self.assertEqual(len(game.board[0]), 4)
        
        # Проверяем, что доска содержит числа от 1 до 15 и 0
        all_numbers = [num for row in game.board for num in row]
        expected_numbers = list(range(16))
        self.assertEqual(sorted(all_numbers), expected_numbers)
    
    def test_find_empty_pos(self):
        """Тест поиска пустой позиции"""
        game = FifteenPuzzle()
        
        # Устанавливаем конкретное состояние доски
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        
        empty_pos = game.find_empty_pos()
        self.assertEqual(empty_pos, (3, 3))
        
        # Тест с пустой ячейкой в другой позиции
        game.board = [
            [1, 2, 3, 4],
            [5, 0, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 6]
        ]
        
        empty_pos = game.find_empty_pos()
        self.assertEqual(empty_pos, (1, 1))
    
    def test_move_valid(self):
        """Тест валидных ходов"""
        game = FifteenPuzzle()
        
        # Устанавливаем состояние, где 0 в центре
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 7]
        ]
        
        # Ход вверх (ячейка 6 должна переместиться вниз)
        result = game.move(2, 2)  # Позиция ячейки 6
        self.assertTrue(result)
        self.assertEqual(game.board[1][1], 0)  # 6 переместилась на место 0
        self.assertEqual(game.board[1][2], 6)  # 0 переместилась вниз
    
    def test_move_invalid(self):
        """Тест невалидных ходов"""
        game = FifteenPuzzle()
        
        # Устанавливаем состояние
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        
        # Ход из угла (1,1) - нет соседней пустой ячейки
        result = game.move(1, 1)
        self.assertFalse(result)
        
        # Ход за пределами доски
        result = game.move(0, 1)
        self.assertFalse(result)
        
        result = game.move(5, 1)
        self.assertFalse(result)
    
    def test_move_directions(self):
        """Тест ходов во всех направлениях"""
        game = FifteenPuzzle()
        
        # Тест движения вверх
        game.board = [
            [1, 2, 3, 4],
            [5, 0, 7, 8],
            [9, 6, 11, 12],
            [13, 14, 15, 10]
        ]
        result = game.move(3, 2) 
        self.assertTrue(result)
        self.assertEqual(game.board[1][1], 6)
        self.assertEqual(game.board[2][1], 0)
        
        # Тест движения вниз
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 0, 11, 12],
            [13, 14, 15, 10]
        ]
        result = game.move(2, 2) 
        self.assertTrue(result)
        self.assertEqual(game.board[2][1], 6)
        self.assertEqual(game.board[1][1], 0)
        
        # Тест движения влево
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 7]
        ]
        result = game.move(2, 4) 
        self.assertTrue(result)
        self.assertEqual(game.board[1][2], 8)
        self.assertEqual(game.board[1][3], 0)
        
        # Тест движения вправо
        game.board = [
            [1, 2, 3, 4],
            [5, 0, 6, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 7]
        ]
        result = game.move(2, 1) 
        self.assertTrue(result)
        self.assertEqual(game.board[1][1], 5)
        self.assertEqual(game.board[1][0], 0)
    
    def test_is_solved(self):
        """Тест проверки решения"""
        game = FifteenPuzzle()
        
        # Решенное состояние
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.assertTrue(game.is_solved())
        
        # Не решенное состояние
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        self.assertFalse(game.is_solved())
        
        # Другое не решенное состояние
        game.board = [
            [2, 1, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.assertFalse(game.is_solved())
    
    def test_get_item(self):
        """Тест получения элемента по индексу"""
        game = FifteenPuzzle()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        
        self.assertEqual(game.get_item((0, 0)), 1)
        self.assertEqual(game.get_item((3, 3)), 0)
        self.assertEqual(game.get_item((1, 2)), 7)
    
    def test_str_representation(self):
        """Тест строкового представления"""
        game = FifteenPuzzle()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        
        expected_output = " 1  2  3  4 \n 5  6  7  8 \n 9 10 11 12 \n13 14 15    \n"
        self.assertEqual(str(game), expected_output)
    
    def test_scramble_changes_board(self):
        """Тест, что перемешивание изменяет доску"""
        game1 = FifteenPuzzle()
        initial_board = [row[:] for row in game1.board]  # Глубокое копирование
        
        # Создаем вторую игру и проверяем, что доски разные
        game2 = FifteenPuzzle()
        
        # С большой вероятностью доски будут разные после перемешивания
        boards_different = any(
            game1.board[i][j] != game2.board[i][j]
            for i in range(4)
            for j in range(4)
        )
        self.assertTrue(boards_different)
    
    def test_scramble_preserves_numbers(self):
        """Тест, что перемешивание сохраняет все числа"""
        game = FifteenPuzzle()
        
        all_numbers = [num for row in game.board for num in row]
        expected_numbers = list(range(16))
        
        self.assertEqual(sorted(all_numbers), expected_numbers)


class TestFifteenPuzzleIntegration(unittest.TestCase):
    """Интеграционные тесты игры"""
    
    def test_multiple_moves(self):
        """Тест последовательности ходов"""
        game = FifteenPuzzle()
        
        # Устанавливаем конкретное состояние
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 0],
            [13, 14, 15, 12]
        ]
        
        # Ход 1: перемещаем 12 вверх
        result1 = game.move(4, 4)
        self.assertTrue(result1)
        self.assertEqual(game.board[2][3], 12)
        self.assertEqual(game.board[3][3], 0)
        
        # Ход 2: перемещаем 15 вправо
        result2 = game.move(4, 3)
        self.assertTrue(result2)
        self.assertEqual(game.board[3][3], 15)
        self.assertEqual(game.board[3][2], 0)
    
    def test_solve_simple_puzzle(self):
        """Тест решения простой головоломки"""
        game = FifteenPuzzle()
        
        # Почти решенное состояние - нужно сделать один ход
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        
        self.assertFalse(game.is_solved())
        
        # Делаем ход для решения
        result = game.move(4, 4)  # Перемещаем 15 влево
        self.assertTrue(result)
        self.assertTrue(game.is_solved())


class TestFifteenPuzzleEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""
    
    def test_move_from_empty_cell(self):
        """Тест хода из пустой ячейки"""
        game = FifteenPuzzle()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        
        # Пытаемся переместить пустую ячейку
        result = game.move(4, 3)
        self.assertFalse(result)  # Не должно быть возможности переместить 0
    
    def test_corner_moves(self):
        """Тест ходов из угловых ячеек"""
        game = FifteenPuzzle()
        
        # Пустая ячейка в правом нижнем углу
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        
        # Ход из левого нижнего угла (13) - не должен работать
        result = game.move(4, 1)
        self.assertFalse(result)
        
        # Ход из правого верхнего угла (4) - не должен работать
        result = game.move(1, 4)
        self.assertFalse(result)
        
        # Ход из ячейки над пустой (15) - должен работать
        result = game.move(4, 3)
        self.assertTrue(result)
    
    def test_boundary_positions(self):
        """Тест граничных позиций"""
        game = FifteenPuzzle()
        
        # Проверяем ходы на границах
        result = game.move(0, 1)  # Слишком маленькая строка
        self.assertFalse(result)
        
        result = game.move(1, 0)  # Слишком маленький столбец
        self.assertFalse(result)
        
        result = game.move(5, 1)  # Слишком большая строка
        self.assertFalse(result)
        
        result = game.move(1, 5)  # Слишком большой столбец
        self.assertFalse(result)


class TestGameInputOutput(unittest.TestCase):
    """Тесты ввода-вывода игры"""
    
    def test_value_error_handling(self):
        """Тест обработки неверного ввода"""
        # Создаем игру
        game = FifteenPuzzle()
        
        # Сохраняем исходное состояние доски
        original_board = [row[:] for row in game.board]
        
        # Пытаемся сделать ход с неверными координатами
        result = game.move("invalid", "input")
        
        # Доска не должна измениться
        self.assertEqual(game.board, original_board)
    
    @patch('builtins.input', side_effect=['1', '1'])
    @patch('builtins.print')
    def test_game_loop_single_move(self, mock_print, mock_input):
        """Тест одного хода в игровом цикле"""
        # Этот тест проверяет логику, аналогичную основной игре
        game = FifteenPuzzle()
        
        # Устанавливаем простое состояние для тестирования
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ]
        
        # Пытаемся сделать ход
        try:
            row = int("1")
            col = int("1")
            result = game.move(row, col)
            # Проверяем что move был вызван
            self.assertIsInstance(result, bool)
        except ValueError:
            self.fail("ValueError was raised unexpectedly")


def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику
    print(f"\nТестов запущено: {result.testsRun}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Провалов: {len(result.failures)}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)