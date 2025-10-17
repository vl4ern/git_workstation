import unittest
import sys
import io
from post_machine import Tape, Rule, Program, Post_machine

class TestTape(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации ленты"""
        tape = Tape()
        self.assertEqual(tape.cells, ['0'])
        self.assertEqual(tape.position, 0)
    
    def test_initialization_with_data(self):
        """Тест инициализации ленты с данными"""
        tape = Tape("101")
        self.assertEqual(tape.cells, ['1', '0', '1'])
        self.assertEqual(tape.position, 0)
    
    def test_get_current(self):
        """Тест получения текущего значения"""
        tape = Tape("101")
        self.assertEqual(tape.get_current(), '1')
        
        tape.position = 1
        self.assertEqual(tape.get_current(), '0')
        
        tape.position = 5  # Вне границ
        self.assertEqual(tape.get_current(), '0')
    
    def test_set_current(self):
        """Тест установки значения"""
        tape = Tape("101")
        
        tape.set_current('0')
        self.assertEqual(tape.cells[0], '0')
        
        tape.position = 1
        tape.set_current('1')
        self.assertEqual(tape.cells[1], '1')
        
        # Тест расширения ленты вправо
        tape.position = 5
        tape.set_current('1')
        self.assertEqual(len(tape.cells), 6)
        self.assertEqual(tape.cells[5], '1')
        
        # Тест расширения ленты влево
        tape.position = -2
        tape.set_current('1')
        self.assertEqual(tape.position, 0)
        self.assertEqual(tape.cells[0], '1')
    
    def test_move_left(self):
        """Тест движения влево"""
        tape = Tape("101")
        tape.position = 1
        
        tape.move_left()
        self.assertEqual(tape.position, 0)
        
        # Движение за левую границу
        tape.move_left()
        self.assertEqual(tape.position, 0)
        self.assertEqual(len(tape.cells), 4)  # Добавилась ячейка слева
    
    def test_move_right(self):
        """Тест движения вправо"""
        tape = Tape("101")
        
        tape.move_right()
        self.assertEqual(tape.position, 1)
        
        # Движение за правую границу
        tape.position = 2
        tape.move_right()
        self.assertEqual(tape.position, 3)
        self.assertEqual(len(tape.cells), 4)
    
    def test_load_from_stream(self):
        """Тест загрузки из потока"""
        tape = Tape()
        stream = io.StringIO("1101\n")
        tape.load_from_stream(stream)
        self.assertEqual(tape.cells, ['1', '1', '0', '1'])
        self.assertEqual(tape.position, 0)
        
        # Пустой поток
        tape = Tape("existing")
        stream = io.StringIO("\n")
        tape.load_from_stream(stream)
        self.assertEqual(tape.cells, ['0'])
    
    def test_str_representation(self):
        """Тест строкового представления"""
        tape = Tape("101")
        tape.position = 1
        self.assertEqual(str(tape), " 1 [0] 1 ")


class TestRule(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации правила"""
        rule = Rule(1, '1', 'X', 'V')
        self.assertEqual(rule.number, 1)
        self.assertEqual(rule.condition, '1')
        self.assertEqual(rule.action_true, 'X')
        self.assertEqual(rule.action_false, 'V')
    
    def test_execute_with_condition_true(self):
        """Тест выполнения правила при истинном условии"""
        rule = Rule(1, '1', 'X', 'V')
        tape = Tape("1")
        action = rule.execute(tape)
        self.assertEqual(action, 'X')
    
    def test_execute_with_condition_false(self):
        """Тест выполнения правила при ложном условии"""
        rule = Rule(1, '1', 'X', 'V')
        tape = Tape("0")
        action = rule.execute(tape)
        self.assertEqual(action, 'V')
    
    def test_str_representation(self):
        """Тест строкового представления правила"""
        rule = Rule(1, '1', 'X', 'V')
        self.assertEqual(str(rule), "1: 1 -> X; !1 -> V")


class TestProgram(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации программы"""
        program = Program()
        self.assertEqual(program.rules, {})
        self.assertEqual(program.current_rule, 1)
    
    def test_add_rule(self):
        """Тест добавления правила"""
        program = Program()
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        self.assertIn(1, program.rules)
        self.assertEqual(program.rules[1], rule)
    
    def test_remove_rule(self):
        """Тест удаления правила"""
        program = Program()
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        
        program.remove_rule(1)
        self.assertNotIn(1, program.rules)
        
        # Удаление несуществующего правила
        program.remove_rule(999)  # Не должно вызывать ошибку
    
    def test_get_rule(self):
        """Тест получения правила"""
        program = Program()
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        
        self.assertEqual(program.get_rule(1), rule)
        self.assertIsNone(program.get_rule(999))
    
    def test_view_rules(self):
        """Тест просмотра правил"""
        program = Program()
        rule1 = Rule(1, '1', 'X', 'V')
        rule2 = Rule(2, '0', 'R', 'L')
        program.add_rule(rule1)
        program.add_rule(rule2)
        
        expected_output = "1: 1 -> X; !1 -> V\n2: 0 -> R; !0 -> L"
        self.assertEqual(program.view_rules(), expected_output)
    
    def test_load_from_stream(self):
        """Тест загрузки программы из потока"""
        program = Program()
        stream = io.StringIO("1: 1 -> X; 0 -> V\n2: 1 -> R; 0 -> L\n")
        program.load_from_stream(stream)
        
        self.assertEqual(len(program.rules), 2)
        self.assertIn(1, program.rules)
        self.assertIn(2, program.rules)
        
        rule1 = program.rules[1]
        self.assertEqual(rule1.condition, '1')
        self.assertEqual(rule1.action_true, 'X')
        self.assertEqual(rule1.action_false, 'V')
    
    def test_load_from_stream_with_comments(self):
        """Тест загрузки программы с комментариями"""
        program = Program()
        stream = io.StringIO("# Комментарий\n1: 1 -> X; 0 -> V\n\n# Еще комментарий\n")
        program.load_from_stream(stream)
        
        self.assertEqual(len(program.rules), 1)
        self.assertIn(1, program.rules)
    
    def test_load_from_stream_invalid_format(self):
        """Тест загрузки программы с неверным форматом"""
        program = Program()
        stream = io.StringIO("invalid format\n")
        
        # Не должно вызывать исключение
        program.load_from_stream(stream)
        self.assertEqual(len(program.rules), 0)
    
    def test_str_representation(self):
        """Тест строкового представления программы"""
        program = Program()
        rule1 = Rule(1, '1', 'X', 'V')
        rule2 = Rule(2, '0', 'R', 'L')
        program.add_rule(rule1)
        program.add_rule(rule2)
        
        expected_output = "1: 1 -> X; !1 -> V\n2: 0 -> R; !0 -> L"
        self.assertEqual(str(program), expected_output)


class TestPostMachine(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации машины Поста"""
        machine = Post_machine()
        self.assertIsInstance(machine.tape, Tape)
        self.assertIsInstance(machine.program, Program)
        self.assertFalse(machine.halted)
        self.assertEqual(machine.step_count, 0)
    
    def test_load_tape_from_stream(self):
        """Тест загрузки ленты из потока"""
        machine = Post_machine()
        stream = io.StringIO("101\n")
        machine.load_tape_from_stream(stream)
        self.assertEqual(machine.tape.cells, ['1', '0', '1'])
    
    def test_load_program_from_stream(self):
        """Тест загрузки программы из потока"""
        machine = Post_machine()
        stream = io.StringIO("1: 1 -> X; 0 -> V\n2: 1 -> R; 0 -> L\n")
        machine.load_program_from_stream(stream)
        self.assertEqual(len(machine.program.rules), 2)
    
    def test_execute_step_erase_mark(self):
        """Тест выполнения шага - стирание метки"""
        machine = Post_machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.get_current(), '0')
        self.assertEqual(machine.program.current_rule, 2)
        self.assertEqual(machine.step_count, 1)
    
    def test_execute_step_set_mark(self):
        """Тест выполнения шага - установка метки"""
        machine = Post_machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.get_current(), '1')
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_execute_step_move_right(self):
        """Тест выполнения шага - движение вправо"""
        machine = Post_machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'R', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.position, 1)
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_execute_step_move_left(self):
        """Тест выполнения шага - движение влево"""
        machine = Post_machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', 'L'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.position, 0)  # Осталось на 0 из-за границы
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_execute_step_conditional_jump(self):
        """Тест выполнения шага - условный переход"""
        machine = Post_machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '?3', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.program.current_rule, 3)
    
    def test_execute_step_stop(self):
        """Тест выполнения шага - останов"""
        machine = Post_machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', '!'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
    
    def test_execute_step_unconditional_jump(self):
        """Тест выполнения шага - безусловный переход"""
        machine = Post_machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '3', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.program.current_rule, 3)
    
    def test_execute_step_invalid_action(self):
        """Тест выполнения шага - неверное действие"""
        machine = Post_machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'invalid', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
    
    def test_execute_step_no_rule(self):
        """Тест выполнения шага - правило не найдено"""
        machine = Post_machine()
        machine.program.current_rule = 999
        
        result = machine.execute_step()
        self.assertFalse(result)
        self.assertTrue(machine.halted)
    
    def test_execute_step_already_halted(self):
        """Тест выполнения шага - машина уже остановлена"""
        machine = Post_machine()
        machine.halted = True
        
        result = machine.execute_step()
        self.assertFalse(result)
    
    def test_execute_all(self):
        """Тест выполнения всей программы"""
        machine = Post_machine()
        machine.tape = Tape("1")
        
        # Простая программа: стереть метку и остановиться
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        machine.program.add_rule(Rule(2, '1', '!', '!'))
        
        machine.execute_all()
        
        self.assertTrue(machine.halted)
        self.assertEqual(machine.tape.get_current(), '0')
        self.assertEqual(machine.step_count, 2)
    
    def test_get_state(self):
        """Тест получения состояния машины"""
        machine = Post_machine()
        machine.tape = Tape("101")
        machine.step_count = 5
        machine.program.current_rule = 3
        
        state = machine.get_state()
        expected_state = {
            'step': 5,
            'current_rule': 3,
            'tape': "[1] 0  1 ",
            'halted': False
        }
        self.assertEqual(state, expected_state)
    
    def test_str_representation(self):
        """Тест строкового представления машины"""
        machine = Post_machine()
        machine.tape = Tape("101")
        machine.step_count = 5
        machine.program.current_rule = 3
        
        expected_str = "Шаг: 5, Правило: 3, Лента: [1] 0  1 , Остановлена: False"
        self.assertEqual(str(machine), expected_str)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_complete_program_execution(self):
        """Тест полного выполнения программы"""
        machine = Post_machine()
        
        # Загружаем ленту и программу как в основном сценарии
        tape_stream = io.StringIO("101\n")
        program_stream = io.StringIO("1: 1 -> X; 0 -> V\n2: 1 -> R; 0 -> L\n3: 1 -> ?1; 0 -> !\n")
        
        machine.load_tape_from_stream(tape_stream)
        machine.load_program_from_stream(program_stream)
        
        # Выполняем всю программу
        machine.execute_all()
        
        # Проверяем конечное состояние
        self.assertTrue(machine.halted)
        self.assertEqual(machine.step_count, 3)
        self.assertEqual(str(machine.tape), "[0] 0  0  1 ")
    
    def test_program_with_complex_logic(self):
        """Тест программы со сложной логикой"""
        machine = Post_machine()
        
        # Программа, которая инвертирует все биты
        tape_stream = io.StringIO("101\n")
        program_stream = io.StringIO("""
            1: 1 -> X; 0 -> V
            2: 1 -> R; 0 -> R  
            3: 1 -> ?1; 0 -> ?
        """)
        
        machine.load_tape_from_stream(tape_stream)
        machine.load_program_from_stream(program_stream)
        
        # Запускаем на несколько шагов
        for _ in range(10):
            if not machine.execute_step():
                break
        
        # Проверяем, что программа работает (не обязательно завершилась)
        self.assertGreater(machine.step_count, 0)


if __name__ == '__main__':
    # Запуск тестов с отчетом о покрытии
    unittest.main(verbosity=2)