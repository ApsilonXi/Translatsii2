import re

def evaluate_expression(expression):
    try:
        rpn = to_rpn(expression)
        print("Обратная польская запись:", rpn)
        result = evaluate_rpn(rpn)
        print("Результат:", result)
    except ValueError as ve:
        print("Ошибка:", ve)
    except ZeroDivisionError as zde:
        print("Ошибка:", zde)

# Преобразование в обратную польскую запись (алгоритм сортировочной станции)
def to_rpn(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []
    tokens = tokenize(expression)
    
    if not tokens:
        raise ValueError("Неверное выражение. Пустое или содержит недопустимые символы.")
    
    for token in tokens:
        if re.match(r'^\d+(\.\d+)?$', token):  # Если это число
            output.append(token)
        elif token in precedence:  # Если это оператор
            while (operators and operators[-1] != '(' and
                   precedence.get(operators[-1], 0) >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':  # Открывающая скобка
            operators.append(token)
        elif token == ')':  # Закрывающая скобка
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators or operators.pop() != '(':
                raise ValueError("Несоответствие скобок.")
    
    while operators:
        if operators[-1] == '(':
            raise ValueError("Несоответствие скобок.")
        output.append(operators.pop())
    
    return output

# Лексический анализ (разделение на токены)
def tokenize(expression):
    # Поддержка чисел, операторов и скобок
    pattern = r'\d+\.\d+|\d+|[+\-*/()]'
    tokens = re.findall(pattern, expression)

    # Проверка на правильное расположение операций и скобок
    for i in range(len(tokens)):
        if tokens[i] in '+-*/':
            # Проверка, чтобы операторы не стояли в начале или в конце выражения
            if i == 0 or i == len(tokens) - 1:
                raise ValueError("Оператор не может находиться в начале или конце выражения.")
            # Проверка, чтобы не было двух операторов подряд
            if tokens[i - 1] in '+-*/' or tokens[i + 1] in '+-*/':
                raise ValueError("Два оператора не могут стоять подряд.")
        elif tokens[i] == '(':
            # Проверка, чтобы после открывающей скобки не было оператора или закрывающей скобки
            if i < len(tokens) - 1 and tokens[i + 1] in '*/':
                raise ValueError("После открывающей скобки не может идти оператор '*' или '/'.")
        elif tokens[i] == ')':
            # Проверка, чтобы перед закрывающей скобкой не было оператора
            if i > 0 and tokens[i - 1] in '+-*/(':
                raise ValueError("Перед закрывающей скобкой не может быть оператора или открывающей скобки.")

    return tokens

# Вычисление выражения в обратной польской записи
def evaluate_rpn(rpn):
    stack = []
    
    for token in rpn:
        if re.match(r'^\d+(\.\d+)?$', token):  # Число
            stack.append(float(token))
        else:  # Оператор
            if len(stack) < 2:
                raise ValueError("Ошибка в вычислениях.")
            b, a = stack.pop(), stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль.")
                stack.append(a / b)
    
    if len(stack) != 1:
        raise ValueError("Ошибка в вычислениях.")
    
    return stack[0]

if __name__ == "__main__":
    expression = input("Введите арифметическое выражение: ")
    evaluate_expression(expression)
