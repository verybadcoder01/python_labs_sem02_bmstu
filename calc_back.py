import math
from enum import Enum
import matplotlib.pyplot as plt


# These functions are not present in math for some reason
def ctan(x):
    return 1 / math.tan(x)

def acctan(x):
    return math.atan(1 / x)

def ctanh(x):
    return 1 / math.tanh(x)

def arctanh(x):
    return math.atanh(1 / x)

# Basic mathematical functions that this program supports
BASE_FUNCTIONS = {"sqrt": math.sqrt, "cos": math.cos, "sin": math.sin, "tg": math.tan, "ctg": ctan, "acos": math.acos,
                  "asin": math.asin, "arctg": math.atan, "arcctg": acctan, "ln": math.log, "sh": math.sinh,
                  "ch": math.cosh, "th": math.tanh, "cth": ctanh,
                  "arsh": math.asinh, "arch": math.acosh, "arth": math.atanh, "arcth": arctanh}

BASE_OPERATIONS = ["*", "+", "-", "/", "^", "(", ")"]

class NewtonMethodErrors(Enum):
    ZERO_DF = 1

class Function:
    def __init__(self, expr):
        self.expression = expr

    def function_at_x(self, value):
        if isinstance(value, float):
            value = f"{value:.10f}"
        else:
            value = str(value)
        func_point = self.expression.replace('x', value)
        parser = Parser(func_point)
        return parser.parse()

    def nth_derivative(self, x, dx_step, n=1):
        if n == 0:
            return self.function_at_x(x)
        if n == 1:
            point1_func = self.function_at_x(x)
            point2_func = self.function_at_x(x + dx_step)
            return (point2_func - point1_func) / dx_step
        return (self.nth_derivative(x + dx_step, dx_step, n - 1) - self.nth_derivative(x, dx_step, n - 1)) / dx_step

class Parser:
    def __init__(self, expression):
        self.tokens = self.tokenize(expression)
        self.position = 0

    def tokenize(self, expression):
        tokens = []
        current_number = ''
        i = 0
        # Negative numbers with - in the beginning might be a problem
        expression = expression.replace("--", "")
        while i < len(expression):
            char = expression[i]
            if char.isdigit() or char == '.' or (len(current_number) == 0 and char == '-' and (i + 1 < len(expression) and expression[i + 1].isdigit())):
                current_number += char
            else:
                if current_number:
                    tokens.append(float(current_number))
                    current_number = ''
                if char in BASE_OPERATIONS:
                    tokens.append(char)
                elif char.isalpha():
                    j = i
                    cur_token = ""
                    while j < len(expression) and expression[j].isalpha() and not expression[j] in BASE_OPERATIONS:
                        cur_token += expression[j]
                        j += 1
                    tokens.append(cur_token)
                    i = j - 1
            i += 1
        if current_number:
            tokens.append(float(current_number))
        return tokens

    def parse(self):
        return self.expression()

    def expression(self):
        result = self.term()
        while self.position < len(self.tokens) and self.tokens[self.position] in ('+', '-'):
            op = self.tokens[self.position]
            self.position += 1
            right = self.term()
            if op == '+':
                result += right
            elif op == '-':
                result -= right
        return result

    def term(self):
        result = self.factor()
        while self.position < len(self.tokens) and self.tokens[self.position] in ('*', '/', '^'):
            op = self.tokens[self.position]
            self.position += 1
            right = self.factor()
            if op == '^':
                result **= right
            elif op == '*':
                result *= right
            elif op == '/':
                result /= right
        return result

    def factor(self):
        if self.tokens[self.position] == '(':
            self.position += 1
            result = self.expression()
            self.position += 1
            return result
        elif isinstance(self.tokens[self.position], float):
            result = self.tokens[self.position]
            self.position += 1
            return result
        elif isinstance(self.tokens[self.position], str):
            func = self.tokens[self.position]
            self.position += 1
            if func in BASE_FUNCTIONS.keys():
                arg = self.factor()
                return BASE_FUNCTIONS[func](arg)
        raise ValueError("Invalid expression")


class NewtonRootFinder:
    def __init__(self, func, deriv_level, seg_left, seg_right, step, precision, max_iterations):
        self.function = func
        self.derivative = deriv_level
        self.seg_left = seg_left
        self.seg_right = seg_right
        self.step = step
        self.precision = precision
        self.max_it = max_iterations
        self.__dx_step = 1e-6

    def one_root_segment(self):
        x = self.seg_left
        while x <= self.seg_right:
            fx = self.function.nth_derivative(x, self.__dx_step, self.derivative)
            fx_step = self.function.nth_derivative(x + self.step, self.__dx_step, self.derivative)
            if fx * fx_step < 0:
                yield x, x + self.step
            elif abs(fx * fx_step) <= 1e-7:
                yield x + self.step * 0.5, x + self.step * 1.5
            x += self.step
        return None

    def function_roots(self):
        result = []
        for seg in self.one_root_segment():
            if seg:
                cur_x = (seg[0] + seg[1]) / 2
            else:
                return result
            for it_cnt in range(self.max_it):
                cur_fx = self.function.nth_derivative(cur_x, self.__dx_step, self.derivative)
                cur_dfx = self.function.nth_derivative(cur_x, self.__dx_step, self.derivative + 1)
                if abs(cur_dfx) <= 1e-7:
                    result.append([len(result) + 1, seg[0], seg[1], "-", "-", it_cnt + 1, NewtonMethodErrors.ZERO_DF])
                    break
                next_x = cur_x - cur_fx / cur_dfx
                if abs(next_x - cur_x) < self.precision and seg[0] <= next_x <= seg[1]:
                    result.append([len(result) + 1, seg[0], seg[1], next_x, self.function.nth_derivative(next_x, self.__dx_step, self.derivative), it_cnt + 1, 0])
                    break
                cur_x = next_x
        return result

class GraphBuilder:
    def __init__(self, func, seg_left, seg_right, prec):
        self.function = Function(func)
        self.seg_left = seg_left
        self.seg_right = seg_right
        self.precision = prec
        self.__dx_step = 1e-6

    def plot(self, roots):
        xs = []
        curx = self.seg_left
        while curx <= self.seg_right:
            xs.append(curx)
            curx += 0.001
        newtonFinder = NewtonRootFinder(self.function, 1, self.seg_left, self.seg_right, 0.01, self.precision, 20)
        roots_one_dx = newtonFinder.function_roots()
        zero_dx = [[i[3], self.function.function_at_x(i[3])] for i in roots_one_dx if i[-1] == 0]
        newtonFinder.derivative = 2
        roots_second_dx = newtonFinder.function_roots()
        zero_second_dx = [[i[3], self.function.function_at_x(i[3])] for i in roots_second_dx if i[-1] == 0]
        ys = [self.function.function_at_x(i) for i in xs]
        plt.plot(xs, ys, label="Функция f(x)")
        if zero_dx:
            plt.scatter(*zip(*zero_dx), color='blue', s=25, label="Точки экстремума")
        if zero_second_dx:
            plt.scatter(*zip(*zero_second_dx), color='red', s=50, label="Точки перегиба")
        if roots:
            plt.scatter(*zip(*roots), color='green', s=25, label="Корни")
        plt.grid(True, which='both')
        plt.legend()
        plt.savefig("graph.png")
        return "graph.png"
