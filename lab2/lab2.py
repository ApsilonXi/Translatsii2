import re

class Lexer:
    def __init__(self, rule_file):
        self.rules = self.load_rules(rule_file)

    def load_rules(self, rule_file):
        rules = {}
        try:
            with open(rule_file, 'r') as file:
                for line in file:
                    lexeme, pattern = line.strip().split(';')
                    rules[lexeme] = re.compile(pattern)
        except FileNotFoundError:
            print(f"Файл {rule_file} не найден. Использование пустого набора правил.")
        return rules

    def add_rule(self, lexeme, pattern):
        if lexeme in self.rules:
            print(f"Правило для лексемы '{lexeme}' уже существует. Обновление правила.")
        self.rules[lexeme] = re.compile(pattern)

    def remove_rule(self, lexeme):
        if lexeme in self.rules:
            del self.rules[lexeme]
            print(f"Правило для лексемы '{lexeme}' удалено.")
        else:
            print(f"Правило для лексемы '{lexeme}' не найдено.")

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            matched = False
            for lexeme, pattern in sorted(self.rules.items(), key=lambda x: -len(x[1].pattern)):
                match = pattern.match(text, position)
                if match:
                    tokens.append(f"<{lexeme},{match.group(0)}>")
                    position = match.end()
                    matched = True
                    break
            if not matched:
                self.handle_error(text, position)
                break
        return tokens

    def handle_error(self, text, position):
        error_char = text[position]
        print(f"Ошибка: неожиданный символ '{error_char}' в позиции {position}.")

def main():
    lexer = Lexer('lab2/rules.txt')
    lexer.add_rule('str', r'"([^"\\]*(?:\\.[^"\\]*)*)"')

    input_string = input('Введите строку: ')
    
    try:
        tokens = lexer.tokenize(input_string)
        print(''.join(tokens))
    except Exception as e:
        print(f"Возникла ошибка: {e}")

if __name__ == "__main__":
    main()