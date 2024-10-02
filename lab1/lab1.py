import re

class FiniteAutomaton:
    def __init__(self, transition_file):
        self.transitions = {}
        self.final_states = set()
        self.load_transitions(transition_file)

    def load_transitions(self, transition_file):
        try:
            with open(transition_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(';')
                    if len(parts) == 3:
                        state_from, symbol, state_to = parts
                        if state_from not in self.transitions:
                            self.transitions[state_from] = {}
                        self.transitions[state_from][symbol] = state_to
        except FileNotFoundError:
            print(f"Ошибка: файл {transition_file} не найден.")

    def is_final_state(self, state):
        return state.startswith('qF')  # Определяем конечные состояния по префиксу

    def process_string(self, input_string):
        # Проверка на корректность строки
        if not re.fullmatch(r'\(\d+;\d+;\d+\)', input_string):
            return "Некорректная строка"

        current_state = 'q0'
        symbols = input_string.strip('()').split(';')

        for symbol in symbols:
            if symbol in self.transitions.get(current_state, {}):
                current_state = self.transitions[current_state][symbol]
            else:
                return "Перехода не существует"

        return "Конечное состояние достигнуто" if self.is_final_state(current_state) else "Конечное состояние не достигнуто"

def main():
    transition_file = "lab1/transitions.txt"
    automaton = FiniteAutomaton(transition_file)

    choice = input("Хотите проверить строки из файла (ф) или ввести одну строку (с)? (ф/с): ").strip().lower()

    if choice == 'ф':
        input_file = "lab1/input.txt"
        try:
            with open(input_file, 'r') as file:
                for line in file:
                    result = automaton.process_string(line.strip())
                    print(f"Строка {line.strip()}: {result}")
        except FileNotFoundError:
            print(f"Ошибка: файл {input_file} не найден.")
    elif choice == 'с':
        input_string = input("Введите строку для проверки: ")
        result = automaton.process_string(input_string)
        print(result)
    else:
        print("Некорректный выбор.")

if __name__ == "__main__":
    main()