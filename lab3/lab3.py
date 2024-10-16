def parse_grammar(file_path):
    grammar = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:  # Игнорируем пустые строки
                continue
            parts = line.split('>')
            lhs = parts[0].strip()
            productions = parts[1].strip().split('|')
            if lhs not in grammar:
                grammar[lhs] = []
            for production in productions:
                grammar[lhs].append(production.strip())
    return grammar

class NDPA:
    def __init__(self, grammar):
        self.grammar = grammar
        self.stack = []
        self.configuration_log = []

    def analyze(self, input_string):
        self.stack.append('E')  # Начинаем с начального символа (в данном случае 'E')
        self.configuration_log.append((self.stack.copy(), input_string))
        return self._process(input_string)

    def _process(self, input_string):
        if not self.stack:
            return not input_string  # Если стек пуст, мы проверяем, что строка также пустая
        
        current_symbol = self.stack.pop()
        
        if current_symbol in self.grammar:  # Если текущий символ — нетерминал
            for production in self.grammar[current_symbol]:
                self.stack.extend(reversed(production))  # Добавляем в стек продукцию
                self.configuration_log.append((self.stack.copy(), input_string))
                if self._process(input_string):
                    return True
                # Если анализ не удался, возвращаем стек и строку к предыдущему состоянию
            self.stack.append(current_symbol)  # Возвращаем текущий символ в стек
            return False
        
        elif current_symbol == '~' and input_string and input_string[0] == ' ':
            return self._process(input_string[1:])  # Игнорируем пробелы
        elif input_string and current_symbol == input_string[0]:
            return self._process(input_string[1:])  # Если символы совпадают

        self.stack.append(current_symbol)  # Возвращаем текущий символ в стек, если ничего не сработало
        return False

    def print_configuration_log(self):
        for stack, remaining in self.configuration_log:
            print(f"Стек: {stack}, Остальная строка: '{remaining}'")

class NDPA:
    def __init__(self, grammar):
        self.grammar = grammar
        self.stack = []
        self.configuration_log = []

    def analyze(self, input_string):
        self.stack.append('E')  # Начинаем с начального символа (в данном случае 'E')
        self.configuration_log.append((self.stack.copy(), input_string))
        return self._process(input_string)

    def _process(self, input_string):
        if not self.stack:
            return not input_string  # Если стек пуст, мы проверяем, что строка также пустая
        
        current_symbol = self.stack.pop()
        
        if current_symbol in self.grammar:  # Если текущий символ — нетерминал
            for production in self.grammar[current_symbol]:
                self.stack.extend(reversed(production))  # Добавляем в стек продукцию
                self.configuration_log.append((self.stack.copy(), input_string))
                if self._process(input_string):
                    return True
                # Если анализ не удался, возвращаем стек и строку к предыдущему состоянию
            self.stack.append(current_symbol)  # Возвращаем текущий символ в стек
            return False
        
        elif current_symbol == '~' and input_string and input_string[0] == ' ':
            return self._process(input_string[1:])  # Игнорируем пробелы
        elif input_string and current_symbol == input_string[0]:
            return self._process(input_string[1:])  # Если символы совпадают

        self.stack.append(current_symbol)  # Возвращаем текущий символ в стек, если ничего не сработало
        return False

    def print_configuration_log(self):
        for stack, remaining in self.configuration_log:
            print(f"Стек: {stack}, Остальная строка: '{remaining}'")

def menu():
    choice = input('Выберите файл лексем:\n1. Грамматика 1\n2. Грамматика 2\n3. Грамматика 3\n')
    match choice:
        case '1':
            # a - b / c
            # m a / c b -
            main('lab3/grammar1.txt')
        case '2':
            # a0x
            # y2z
            main('lab3/grammar2.txt')
        case '3':
            # ab
            # aaab
            main('lab3/grammar3.txt')

def main(grammar_file):
    test_string = input('Введите строку для анализа: ')   # Замените на необходимую строку для анализа

    grammar = parse_grammar(grammar_file)
    automaton = NDPA(grammar)

    if automaton.analyze(test_string):
        print("Строка допустима.")
    else:
        print("Строка недопустима.")
    
    print("\nКонфигурации во время выполнения:")
    automaton.print_configuration_log()

if __name__ == "__main__":
    menu()