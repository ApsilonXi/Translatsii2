import re

# Классы токенов
TOKENS = [
    ('KEYWORD', r'\b(int|bool|void|main|for|if|return)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('OPERATOR', r'[=<>!]+'),
    ('SEPARATOR', r'[{}();]'),
    ('WHITESPACE', r'\s+'),  # Пробелы и переносы строк
    ('UNKNOWN', r'.'),  # Любой непредусмотренный символ
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for token_type, regex in TOKENS:
                pattern = re.compile(regex)
                match = pattern.match(self.code, self.position)
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':  # Пропускаем пробелы
                        self.tokens.append((token_type, value, self.line, self.column))
                    self.position += len(value)
                    self.update_position(value)
                    break
            if not match:
                raise ValueError(f"Неизвестный символ на строке {self.line}, колонке {self.column}")

    def update_position(self, value):
        if '\n' in value:
            self.line += value.count('\n')
            self.column = 1
        else:
            self.column += len(value)

# Пример использования лексера:
code = """
int main() {
    int a = 5;
    for (int i = 0; i < 10;) {
        if (a == 5) {
            return 1;
        }
    }
}
"""

lexer = Lexer(code)
lexer.tokenize()
for token in lexer.tokens:
    print(token)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self, expected_type=None, expected_value=None):
        token = self.current_token()
        if token is None:
            self.error("Ожидался токен, но найден конец ввода")
            return None
        
        if expected_type and token[0] != expected_type:
            self.error(f"Ожидался {expected_type}, но найдено {token[0]}")
            return None
        
        if expected_value and token[1] != expected_value:
            self.error(f"Ожидалось {expected_value}, но найдено {token[1]}")
            return None

        self.position += 1
        return token

    def error(self, message):
        token = self.current_token()
        if token:
            error_message = f"Ошибка на строке {token[2]}, колонке {token[3]}: {message}"
        else:
            error_message = "Ошибка: конец ввода"
        self.errors.append(error_message)
        # Режим паники: пропускаем следующий токен
        self.position += 1

    # Начало разбора программы
    def parse_program(self):
        self.parse_type()
        self.consume('IDENTIFIER', 'main')
        self.consume('SEPARATOR', '(')
        self.consume('SEPARATOR', ')')
        self.consume('SEPARATOR', '{')
        self.parse_statement()
        self.consume('SEPARATOR', '}')

    def parse_type(self):
        self.consume('KEYWORD')

    def parse_statement(self):
        token = self.current_token()
        if token[0] == 'KEYWORD' and token[1] == 'int':
            self.parse_declaration()
            self.consume('SEPARATOR', ';')
        elif token[0] == 'KEYWORD' and token[1] == 'for':
            self.parse_for()
            self.parse_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'if':
            self.parse_if()
            self.parse_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'return':
            self.consume('KEYWORD', 'return')
            self.consume('NUMBER')
            self.consume('SEPARATOR', ';')
        elif token[0] == 'SEPARATOR' and token[1] == '{':
            self.consume('SEPARATOR', '{')
            self.parse_statement()
            self.consume('SEPARATOR', '}')
        else:
            self.error(f"Неожиданное выражение: {token[1]}")

    def parse_declaration(self):
        self.parse_type()
        self.consume('IDENTIFIER')
        self.consume('OPERATOR', '=')
        self.consume('NUMBER')

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        self.consume('SEPARATOR', '(')
        self.parse_declaration()
        self.consume('SEPARATOR', ';')
        self.parse_expression()
        self.consume('SEPARATOR', ';')
        self.consume('SEPARATOR', ')')

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        self.consume('SEPARATOR', '(')
        self.parse_expression()
        self.consume('SEPARATOR', ')')

    def parse_expression(self):
        token = self.current_token()
        if token[0] == 'IDENTIFIER' or token[0] == 'NUMBER':
            self.consume(token[0])
            self.consume('OPERATOR')
            self.consume('IDENTIFIER')
        else:
            self.error("Ожидалось выражение")

# Пример синтаксического анализа программы:
parser = Parser(lexer.tokens)
parser.parse_program()

if parser.errors:
    print(f"Обнаружено ошибок: {len(parser.errors)}")
    for error in parser.errors:
        print(error)
else:
    print("Программа корректна.")
