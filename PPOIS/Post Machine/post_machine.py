import sys

class Tape:
    # Лента Машины Поста
    def __init__(self, initial_data=""):
        self.cells = list(initial_data) if initial_data else ['0']
        self.position = 0
        
    # ПОлучение значния
    def get_current(self):
        if 0 <= self.position < len(self.cells):
            return self.cells[self.position]
        return '0'
    
    # Проверяем на диапазон
    def set_current(self, value):
        if 0 <= self.position < len(self.cells):
            self.cells[self.position] = value
        else:
            # Расширяем ленту если нужно
            if self.position < 0:
                self.cells = ['0'] * (-self.position) + self.cells
                self.position = 0
            else:
                self.cells.extend(['0'] * (self.position - len(self.cells) + 1))
            self.cells[self.position] = value
    
    
    # Функции передвижение
    def move_left(self):
        self.position -= 1
        if self.position < 0:
            self.cells.insert(0, '0')
            self.position = 0
    
    def move_right(self):
        self.position += 1
        if self.position >= len(self.cells):
            self.cells.append('0')
    
    def load_from_stream(self, stream):
        data = stream.readline().strip()
        self.cells = list(data) if data else ['0']
        self.position = 0
    
    def __str__(self):
        result = []
        for i, cell in enumerate(self.cells):
            if i == self.position:
                result.append(f"[{cell}]")
            else:
                result.append(f" {cell} ")
        return "".join(result)

class Rule:
    def __init__(self, number, condition, action_true, action_false):
        self.number = number
        self.condition = condition  # '1' - метка есть, '0' - метки нет
        self.action_true = action_true
        self.action_false = action_false
    
    def execute(self, tape):
        current_value = tape.get_current()
        
        if current_value == self.condition:
            return self.action_true
        else:
            return self.action_false
    
    def __str__(self):
        return f"{self.number}: {self.condition} -> {self.action_true}; !{self.condition} -> {self.action_false}"

class Program:
    def __init__(self):
        self.rules = {} 
        self.current_rule = 1  
    
    def add_rule(self, rule):
        self.rules[rule.number] = rule
    
    def remove_rule(self, number):
        if number in self.rules:
            del self.rules[number]
    
    def get_rule(self, number):
        return self.rules.get(number)
    
    def view_rules(self):
        return "\n".join(str(rule) for num, rule in sorted(self.rules.items()))
    
    def load_from_stream(self, stream):
        for line in stream:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            try:
                # Формат: номер: условие -> действие_истина; действие_ложь
                parts = line.split(':')
                number = int(parts[0].strip())
                
                actions_part = parts[1].split(';')
                condition_action = actions_part[0].split('->')
                condition = condition_action[0].strip()
                action_true = condition_action[1].strip()
                
                action_false = actions_part[1].split('->')[1].strip()
                
                rule = Rule(number, condition, action_true, action_false)
                self.add_rule(rule)
                
            except (ValueError, IndexError) as e:
                print(f"Ошибка parsing правила: {line}")
                continue
    
    def __str__(self):
        return self.view_rules()

class Post_machine:
    def __init__(self):
        self.tape = Tape()
        self.program = Program()
        self.halted = False
        self.step_count = 0
    
    # потокавая ленты загрузка
    def load_tape_from_stream(self, stream):
        self.tape.load_from_stream(stream)
    
    # потоковая загрузка программы и правил
    def load_program_from_stream(self, stream):
        self.program.load_from_stream(stream)
    
    # один шаг
    def execute_step(self):
        if self.halted:
            return False
        
        current_rule = self.program.get_rule(self.program.current_rule)
        if not current_rule:
            self.halted = True
            return False
        
        action = current_rule.execute(self.tape)
        self.step_count += 1
        
        # Обработка действий
        if action == 'V':  # Поставить метку
            self.tape.set_current('1')
            self.program.current_rule += 1
        elif action == 'X':  # Стереть метку
            self.tape.set_current('0')
            self.program.current_rule += 1
        elif action == 'R':  # Движение вправо
            self.tape.move_right()
            self.program.current_rule += 1
        elif action == 'L':  # Движение влево
            self.tape.move_left()
            self.program.current_rule += 1
        elif action.startswith('?'): 
            try:
                self.program.current_rule = int(action[1:])
            except(ValueError, IndexError):
                self.halted = True
        elif action == '!':  # Остановка
            self.halted = True
        else:  # Простой переход на правило
            try:
                self.program.current_rule = int(action)
            except ValueError:
                self.halted = True
        
        return True
    
    # выполнение всех возможных шагов
    def execute_all(self):
        while self.execute_step():
            pass
    
    # возвращение текующего состояния машины
    def get_state(self):
        return {
            'step': self.step_count,
            'current_rule': self.program.current_rule,
            'tape': str(self.tape),
            'halted': self.halted
        }
    
    # строковый формат предствавления состояния
    def __str__(self):
        state = self.get_state()
        return (f"Шаг: {state['step']}, "
                f"Правило: {state['current_rule']}, "
                f"Лента: {state['tape']}, "
                f"Остановлена: {state['halted']}")

def main():
    if len(sys.argv) < 2:
        print("Использование: python post_machine.py <файл> [-log]")
        sys.exit(1)
    
    filename = sys.argv[1]
    log_mode = len(sys.argv) > 2 and sys.argv[2] == '-log'
    
    try:
        # Создаем и инициализируем машину Поста
        machine = Post_machine()
        
        with open(filename, 'r', encoding='utf-8') as f:
            # Первая строка - начальное состояние ленты
            machine.load_tape_from_stream(f)
            # Остальные строки - программа (набор правил)
            machine.load_program_from_stream(f)
        
        print("Начальное состояние:")
        print(machine)
        print("\nЗагруженные правила:")
        print(machine.program.view_rules())
        print()
        
        if log_mode:
            # Пошаговое выполнение с выводом после каждого шага
            step = 1
            while machine.execute_step():
                print(f"После шага {step}:")
                print(machine)
                step += 1
                print()
        else:
            # Выполнение всей программы
            machine.execute_all()
        
        print("\nФинальное состояние:")
        print(machine)
        
        
        # проверка на существование файла с правилами
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()