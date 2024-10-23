class PDA:
    def __init__(self, grammar):
        self.grammar = self.parse_grammar(grammar)
        self.stack = []
        self.active_states = set()

    @staticmethod
    def parse_grammar(grammar_lines):
        grammar = {}
        for line in grammar_lines:
            line = line.replace(" ", "").replace("~", " ")
            left_part, *right_parts = line.split(">")
            for right_part in right_parts:
                if left_part in grammar:
                    grammar[left_part].append(right_part)
                else:
                    grammar[left_part] = [right_part]
        return grammar

    def analyze(self, input_string):
        self.stack.append("E")  # Начинаем с начального символа грамматики
        input_string += "#"  # Добавляем символ конца строки

        while self.stack:
            current_stack_top = self.stack.pop()
            if current_stack_top == input_string[0]:  # Сравниваем со входной строкой
                input_string = input_string[1:]  # Удаляем символ из входной строки
                self.log_state(input_string)
                if current_stack_top == "#":
                    return True  # Успешное завершение
                continue
            
            if current_stack_top in self.grammar:  # Нетерминал
                for production in self.grammar[current_stack_top]:
                    self.stack.extend(reversed(production))  # Добавляем продукцию в стек в обратном порядке
                    self.log_state(input_string)
            else:
                return False  # Состояние не соответствует ни одному правилу

        return False  # Если стек пуст, но строка не полностью обработана

    def log_state(self, input_string):
        print(f"Current input: {input_string}, Stack: {self.stack}")

# Загружаем грамматики (можно разбить на разные файлы по необходимости)
with open('lab3/grammar.txt', 'r') as f:
    grammar_lines = f.readlines()

grammar = [line.strip() for line in grammar_lines if line.strip()]
pda = PDA(grammar)

# Проверяем строку
strings_to_check = [
    "mab0",     # Верная строка для грамматики 1

]

for test_string in strings_to_check:
    print(f"\nTesting string: {test_string}")
    result = pda.analyze(test_string)
    print(f"Result: {'Accepted' if result else 'Rejected'}")