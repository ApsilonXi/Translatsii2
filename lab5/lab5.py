import re

class Parser:
    def __init__(self, input_code):
        """
        Инициализация парсера с исходным кодом.
        """
        self.input_code = input_code
        self.position = 0
        self.current_token = None
        self.errors = []
        self.tokenize()

    def tokenize(self):
        """
        Разбиение исходного кода на токены с использованием регулярных выражений.
        """
        self.tokens = re.findall(r'\w+|[();{}=><!]', self.input_code)
        self.tokens.append(None)  # Добавляем конечный токен
        self.position = 0
        self.next_token()

    def next_token(self):
        """
        Переход к следующему токену.
        """
        self.current_token = self.tokens[self.position]
        self.position += 1

    def parse(self):
        """
        Метод для парсинга исходного кода.
        """
        if self.current_token in ['int', 'bool', 'void']:
            self.parse_type()
            if self.current_token == 'main':
                self.next_token()
                self.parse_main()
            else:
                self.add_error("Ожидалось 'main' после типа")
        else:
            self.add_error("Ожидался тип (int, bool, void) в начале")

    def parse_type(self):
        """
        Проверка и обработка типа данных.
        """
        if self.current_token in ['int', 'bool', 'void']:
            self.next_token()
        else:
            self.add_error("Ожидался тип (int, bool, void)")

    def parse_main(self):
        """
        Обработка главной функции main().
        """
        if self.current_token == '(':
            self.next_token()
            if self.current_token == ')':
                self.next_token()
                self.parse_block()
            else:
                self.add_error("Ожидалась закрывающая скобка ')' после main")
        else:
            self.add_error("Ожидалась открывающая скобка '(' после main")

    def parse_block(self):
        """
        Обработка блока кода, заключенного в фигурные скобки.
        """
        if self.current_token == '{':
            self.next_token()
            while self.current_token and self.current_token != '}':
                self.parse_statement()
            if self.current_token == '}':
                self.next_token()
            else:
                self.add_error("Ожидалась закрывающая скобка '}'")
        else:
            self.add_error("Ожидалась открывающая скобка '{'")

    def parse_statement(self):
        """
        Обработка различных типов выражений и операторов.
        """
        if self.current_token == 'return':
            self.parse_return_statement()
        elif self.current_token == '{':
            self.parse_block()
        elif self.current_token == 'for':
            self.parse_for_statement()
        elif self.current_token == 'if':
            self.parse_if_statement()
        elif self.current_token:
            self.parse_declaration()
            if self.current_token == ';':
                self.next_token()
            else:
                self.add_error("Ожидалась точка с запятой ';' после оператора")
        else:
            self.add_error("Неожиданный конец выражения")

    def parse_declaration(self):
        """
        Обработка объявления переменной.
        """
        if self.current_token in ['int', 'bool', 'void']:
            self.parse_type()
            if self.current_token and self.is_identifier(self.current_token):
                self.next_token()
                self.parse_assignment()
            else:
                self.add_error("Ожидалось имя переменной после типа")
        else:
            self.add_error("Ожидался тип (int, bool, void) для объявления")

    def parse_assignment(self):
        """
        Обработка оператора присваивания.
        """
        if self.current_token == '=':
            self.next_token()
            if self.current_token.isdigit() or self.is_identifier(self.current_token):
                self.next_token()
            else:
                self.add_error("Ожидалось значение или идентификатор после '='")
        else:
            self.add_error("Ожидался оператор '=' для присваивания")

    def parse_for_statement(self):
        """
        Обработка оператора цикла for.
        """
        if self.current_token == 'for':
            self.next_token()
            if self.current_token == '(':
                self.next_token()
                self.parse_for_declaration()
                self.parse_for_condition()
                self.parse_for_iteration()
                if self.current_token == ')':
                    self.next_token()
                    self.parse_statement()
                else:
                    self.add_error("Ожидалась закрывающая скобка ')' после цикла for")
            else:
                self.add_error("Ожидалась открывающая скобка '(' после 'for'")
        else:
            self.add_error("Ожидалось 'for'")

    def parse_for_declaration(self):
        """
        Обработка объявления переменной в цикле for.
        """
        if self.current_token in ['int', 'bool', 'void']:
            self.parse_declaration()
        else:
            self.add_error("Ожидалось объявление переменной в цикле for")

    def parse_for_condition(self):
        """
        Обработка условного выражения в цикле for.
        """
        if self.current_token == ';':
            self.next_token()
            self.parse_expression()
        else:
            self.add_error("Ожидалась точка с запятой ';' после условия в цикле for")

    def parse_for_iteration(self):
        """
        Обработка выражения итерации в цикле for.
        """
        if self.current_token == ';':
            self.next_token()
            if self.current_token.isdigit() or self.is_identifier(self.current_token):
                self.next_token()
            else:
                self.add_error("Ожидался идентификатор или число в итерации цикла for")

    def parse_if_statement(self):
        """
        Обработка оператора if.
        """
        if self.current_token == 'if':
            self.next_token()
            if self.current_token == '(':
                self.next_token()
                self.parse_expression()
                if self.current_token == ')':
                    self.next_token()
                    self.parse_statement()
                else:
                    self.add_error("Ожидалась закрывающая скобка ')' после условия if")
            else:
                self.add_error("Ожидалась открывающая скобка '(' после 'if'")
        else:
            self.add_error("Ожидалось 'if'")

    def parse_return_statement(self):
        """
        Обработка оператора return.
        """
        if self.current_token == "return":
            self.next_token()
            if self.current_token.isdigit():
                self.next_token()
                if self.current_token == ';':
                    self.next_token()
                else:
                    self.add_error("Ожидалась точка с запятой ';' после return")
            else:
                self.add_error("Ожидалось число после return")

    def parse_expression(self):
        """
        Обработка выражения.
        """
        if self.is_identifier(self.current_token):
            self.next_token()
            self.parse_relational_operator()
        elif self.current_token.isdigit():
            self.next_token()
            self.parse_relational_operator()
        else:
            self.add_error("Ожидался идентификатор или число в выражении")

    def parse_relational_operator(self):
        """
        Обработка оператора сравнения.
        """
        if self.current_token in ['<', '>', '==', '!=']:
            self.next_token()
            if self.is_identifier(self.current_token) or self.current_token.isdigit():
                self.next_token()
            else:
                self.add_error("Ожидался идентификатор или число после оператора сравнения")
        else:
            self.add_error("Ожидался оператор сравнения после идентификатора или числа")

    def is_identifier(self, token):
        """
        Проверка, является ли токен идентификатором.
        """
        return re.match(r'^[a-zA-Z_]\w*$', token) is not None

    def add_error(self, message):
        """
        Добавление ошибки в список ошибок.
        """
        self.errors.append(f"Ошибка на токене '{self.current_token}': {message}")
        self.skip_to_next_semicolon_or_brace()

    def skip_to_next_semicolon_or_brace(self):
        """
        Пропуск токенов до следующего символа ';' или '}'.
        """
        while self.current_token and self.current_token not in [';', '}']:
            self.next_token()
        if self.current_token in [';', '}']:
            self.next_token()

    def get_errors(self):
        """
        Возвращает список ошибок.
        """
        return self.errors


# Пример использования
input_code = """
int main() {
    int b = 10;
    if (b > 7) {
        return 10;
    }
    for (int i = 0; i < 10; i++) {
        int a = 10;
    }
    return 0;
}
"""

parser = Parser(input_code)
parser.parse()

# Вывод результатов
errors = parser.get_errors()
if errors:
    print(f"Количество ошибок: {len(errors)}")
    for error in errors:
        print(error)
else:
    print("Ошибок не найдено.")
