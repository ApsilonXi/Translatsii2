import re

# Класс для хранения токена с типом и значением
class Token:
    def __init__(self, type_, value, line, pos):
        self.type = type_
        self.value = value
        self.line = line
        self.pos = pos

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.pos})"


# Лексический анализатор (токенизатор)
class Lexer:
    def __init__(self, code):
        self.code = code
        self.keywords = {"int", "bool", "void", "for", "if", "return", "main"}
        self.operators = {"=", "<", ">", "==", "!=", "(", ")", "{", "}", ";", ","}
        self.tokens = []
        self.current_line = 1
        self.current_pos = 0  # позиция внутри строки

    def tokenize(self):
        # Регулярное выражение для токенизации
        pattern = re.compile(r'\s*(?:(\d+)|([a-zA-Z_]\w*)|([<>!=]=?|[{}();,])|(.))')
        pos = 0
        while pos < len(self.code):
            match = pattern.match(self.code, pos)
            if not match:
                print(f"Неизвестный символ на строке {self.current_line}, позиция {self.current_pos}: '{self.code[pos]}'")
                pos += 1
                self.current_pos += 1
                continue

            number, identifier, operator, unknown = match.groups()
            
            # Пропуск пробелов и символов новой строки
            if match.group(0).isspace():
                if '\n' in match.group(0):
                    self.current_line += 1
                    self.current_pos = 0  # сброс позиции для новой строки
                else:
                    self.current_pos += len(match.group(0))
                pos = match.end()
                continue

            if number:
                self.tokens.append(Token('NUMBER', number, self.current_line, self.current_pos))
            elif identifier:
                if identifier in self.keywords:
                    self.tokens.append(Token('KEYWORD', identifier, self.current_line, self.current_pos))
                else:
                    self.tokens.append(Token('IDENTIFIER', identifier, self.current_line, self.current_pos))
            elif operator:
                self.tokens.append(Token('OPERATOR', operator, self.current_line, self.current_pos))
            elif unknown:
                print(f"Неизвестный символ на строке {self.current_line}, позиция {self.current_pos}: '{unknown}'")
            
            # Обновление позиции в коде
            pos = match.end()
            self.current_pos += match.end() - match.start()

        return self.tokens


# Синтаксический анализатор
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = 0

    def error(self, message):
        token = self.tokens[self.current] if self.current < len(self.tokens) else Token('EOF', '', -1, -1)
        print(f"Ошибка: {message} на строке {token.line}, позиция {token.pos}")
        self.errors += 1

    def match(self, expected_type=None, expected_value=None):
        if self.current >= len(self.tokens):
            return False
        token = self.tokens[self.current]
        if expected_type and token.type != expected_type:
            return False
        if expected_value and token.value != expected_value:
            return False
        self.current += 1
        return True

    def parse(self):
        # Начало разбора основной функции
        if not self.match('KEYWORD', 'int') and not self.match('KEYWORD', 'bool') and not self.match('KEYWORD', 'void'):
            self.error("Ожидался тип 'int', 'bool' или 'void'")
        if not self.match('KEYWORD', 'main'):
            self.error("Ожидалась функция 'main'")
        if not self.match('OPERATOR', '(') or not self.match('OPERATOR', ')'):
            self.error("Ожидались скобки '()' после 'main'")
        if not self.match('OPERATOR', '{'):
            self.error("Ожидалась открывающая фигурная скобка '{'")

        # Разбираем тело программы
        while not self.match('OPERATOR', '}'):
            self.statement()

        print(f"Синтаксический анализ завершен с {self.errors} ошибками")

    def statement(self):
        if self.match('KEYWORD', 'int') or self.match('KEYWORD', 'bool') or self.match('KEYWORD', 'void'):
            # Декларация переменной
            if not self.match('IDENTIFIER'):
                self.error("Ожидался идентификатор")
            if not self.match('OPERATOR', '='):
                self.error("Ожидался оператор '='")
            if not self.match('NUMBER') and not self.match('IDENTIFIER'):
                self.error("Ожидалось число или идентификатор")
            if not self.match('OPERATOR', ';'):
                self.error("Ожидалась ';' после декларации")
        elif self.match('KEYWORD', 'return'):
            # Оператор return
            if not self.match('NUMBER'):
                self.error("Ожидалось число после 'return'")
            if not self.match('OPERATOR', ';'):
                self.error("Ожидалась ';' после 'return'")
        elif self.match('KEYWORD', 'for'):
            # Оператор for
            if not self.match('OPERATOR', '('):
                self.error("Ожидалась '(' после 'for'")
            self.statement()  # Декларация в for
            if not self.match('OPERATOR', ';'):
                self.error("Ожидалась ';' после декларации в 'for'")
            self.expression()  # Условие в for
            if not self.match('OPERATOR', ';'):
                self.error("Ожидалась ';' после условия в 'for'")
            self.statement()  # Итерация в for
            if not self.match('OPERATOR', ')'):
                self.error("Ожидалась ')' после 'for'")

            # Проверка тела цикла, если оно в фигурных скобках
            if self.match('OPERATOR', '{'):
                while not self.match('OPERATOR', '}'):
                    self.statement()
            else:
                # Ожидаем одну инструкцию, если нет фигурных скобок
                self.statement()
        elif self.match('KEYWORD', 'if'):
            # Оператор if
            if not self.match('OPERATOR', '('):
                self.error("Ожидалась '(' после 'if'")
            self.expression()
            if not self.match('OPERATOR', ')'):
                self.error("Ожидалась ')' после условия в 'if'")
            self.statement()
        else:
            self.error("Ожидался оператор или декларация")

    def expression(self):
        # Разбор простого выражения вида "i < 10"
        if not self.match('IDENTIFIER') and not self.match('NUMBER'):
            self.error("Ожидался идентификатор или число в выражении")
        if not self.match('OPERATOR', '<') and not self.match('OPERATOR', '>') and not self.match('OPERATOR', '==') and not self.match('OPERATOR', '!='):
            self.error("Ожидался оператор сравнения в выражении")
        if not self.match('IDENTIFIER') and not self.match('NUMBER'):
            self.error("Ожидался идентификатор или число после оператора сравнения")




# Основная функция
def main():
    code = """
    int main() { 
        int a = 5; 
        for (int i = 0; i < 10;) { 
            return 3; 
        } 
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Токены:", tokens)
    
    parser = Parser(tokens)
    parser.parse()

if __name__ == "__main__":
    main()
