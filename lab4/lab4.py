import re

class ExpressionEvaluator:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = []

    def tokenize(self):
        # Регулярное выражение для токенов: числа, операторы и скобки
        token_pattern = r'\d+(\.\d+)?|[+\-*/()]'
        self.tokens = re.findall(token_pattern, self.expression)
        return self.tokens

    def shunting_yard(self):
        output = []
        operators = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in self.tokens:
            if re.match(r'\d+(\.\d+)?', token):  # Если токен - число
                output.append(token)
            elif token in precedence:  # Если токен - оператор
                while (operators and operators[-1] != '(' and
                       precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':  # Если токен - открывающая скобка
                operators.append(token)
            elif token == ')':  # Если токен - закрывающая скобка
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if not operators:
                    raise ValueError("Количество скобок не совпадает.")
                operators.pop()  # Удаляем открывающую скобку

        while operators:
            if operators[-1] == '(':
                raise ValueError("Количество скобок не совпадает.")
            output.append(operators.pop())

        return output

    def evaluate_rpn(self, rpn):
        stack = []
        for token in rpn:
            if re.match(r'\d+(\.\d+)?', token):  # Если токен - число
                stack.append(float(token))
            else:  # Если токен - оператор
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ValueError("Деление на ноль.")
                    stack.append(a / b)
        return stack.pop() if stack else 0

    def evaluate(self):
        try:
            self.tokenize()
            rpn = self.shunting_yard()
            result = self.evaluate_rpn(rpn)
            return rpn, result
        except ValueError as e:
            return str(e)

# Пример использования
if __name__ == "__main__":
    expression = input("Введите арифметическое выражение: ")
    evaluator = ExpressionEvaluator(expression)
    output = evaluator.evaluate()
    
    if isinstance(output, tuple):
        rpn, result = output
        print("Обратная польская запись:", ' '.join(rpn))
        print("Результат вычисления:", result)
    else:
        print("Ошибка:", output)