import re

# Функция для преобразования инфиксного выражения в обратную польскую запись
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0, ')': 0}
    output = []
    operators = []

    tokens = tokenize(expression)
    
    for token in tokens:
        if is_number(token):
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators or operators[-1] != '(':
                raise ValueError("Несовпадающие скобки")
            operators.pop()
        else:
            while (operators and precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)

    while operators:
        if operators[-1] == '(':
            raise ValueError("Несовпадающие скобки")
        output.append(operators.pop())

    return output

# Функция для вычисления выражения в обратной польской записи
def evaluate_postfix(postfix):
    stack = []

    for token in postfix:
        if is_number(token):
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise ValueError("Неверное выражение")
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ValueError("Деление на ноль")
                result = a / b
            else:
                raise ValueError(f"Неизвестный оператор {token}")
            
            stack.append(result)

    if len(stack) != 1:
        raise ValueError("Неверное выражение")

    return stack[0]

# Исправленная функция для разбора выражения на токены
def tokenize(expression):
    # Новое регулярное выражение для чисел (целых и дробных), операторов и скобок
    token_pattern = re.compile(r'\d+\.\d+|\d+|[+\-*/()]')
    tokens = token_pattern.findall(expression)
    return tokens

# Функция для проверки, является ли строка числом
def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

# Основная функция программы
def main():
    expression = input("Введите арифметическое выражение: ").strip()

    try:
        postfix = infix_to_postfix(expression)
        print(f"Обратная польская запись: {' '.join(postfix)}")

        result = evaluate_postfix(postfix)
        print(f"Результат: {result}")

    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
