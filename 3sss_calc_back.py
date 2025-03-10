NUM_DIGITS = "0.+-"
NUM_BORDER = "'"
ALLOWED_CALC_INPUT = NUM_DIGITS + NUM_BORDER

ALLOWED_OPERATIONS = "+-"


def balanced_ternary_add_digits(dig1, dig2):
    match (dig1, dig2):
        case ('+', '-') | ('-', '+'):
            return '0', '0'
        case ('+', '0') | ('0', '+'):
            return '+', '0'
        case ('-', '0') | ('0', '-'):
            return '-', '0'
        case ('+', '+'):
            return '-', '+'
        case ('-', '-'):
            return '+', '-'
        case ('0', '0'):
            return '0', '0'


def extract_dec_frac_parts(num):
    parts = num.split('.')
    dec_part = parts[0]
    if len(parts) > 1:
        frac_parts = parts[1]
    else:
        frac_parts = ''
    return dec_part, frac_parts


def balanced_ternary_operation(num1, num2, operation):
    dec_part1, frac_part1 = extract_dec_frac_parts(num1)
    dec_part2, frac_part2 = extract_dec_frac_parts(num2)

    max_dec_length = max(len(dec_part1), len(dec_part2))
    max_frac_length = max(len(frac_part1), len(frac_part2))

    dec_part1 = dec_part1.rjust(max_dec_length, '0')
    dec_part2 = dec_part2.rjust(max_dec_length, '0')
    frac_part1 = frac_part1.ljust(max_frac_length, '0')
    frac_part2 = frac_part2.ljust(max_frac_length, '0')

    num1 = dec_part1 + '.' + frac_part1
    num2 = dec_part2 + '.' + frac_part2

    result = []
    carry = '0'

    num1 = list(num1)
    num2 = list(num2)

    if operation == '-':
        for i in range(len(num2)):
            if num2[i] == '+':
                num2[i] = '-'
            elif num2[i] == '-':
                num2[i] = '+'

    for digit1, digit2 in zip(reversed(num1), reversed(num2)):
        if digit1 == '.' or digit2 == '.':
            result.append('.')
            continue
        next_dig, next_carry = balanced_ternary_add_digits(digit1, digit2)
        next_dig, carry2 = balanced_ternary_add_digits(next_dig, carry)
        next_carry, _ = balanced_ternary_add_digits(next_carry, carry2)
        carry = next_carry
        result.append(next_dig)

    if carry != '0':
        result.append(carry)

    result = ''.join(reversed(result))
    dec_part, frac_part = extract_dec_frac_parts(result)
    dec_part = list(dec_part)
    frac_part = list(frac_part)

    while len(dec_part) > 1 and dec_part[0] == '0':
        dec_part.pop(0)

    while len(frac_part) > 0 and frac_part[-1] == '0':
        frac_part.pop()

    return ''.join(dec_part) + ('.' + ''.join(frac_part) if len(frac_part) > 0 else '')


def calc_balanced_ternary_expression(expr):
    if not expr or expr[0] != NUM_BORDER or expr[-1] != NUM_BORDER:
        raise Exception("Неверный ввод.")
    current_number = ""
    is_number = False
    current_result = ""
    last_operation = ""
    for i in expr:
        if is_number and i in ALLOWED_CALC_INPUT:
            current_number += i
        elif not is_number and i in ALLOWED_OPERATIONS:
            if last_operation:
                if current_result.count('.') > 1 or current_number.count('.') > 1:
                    raise Exception("Неверный ввод.")
                current_result = balanced_ternary_operation(current_result, current_number, last_operation)
            last_operation = i
            current_number = ""
        elif (is_number and i not in ALLOWED_CALC_INPUT) or (
                not is_number and i not in ALLOWED_OPERATIONS) and i != NUM_BORDER:
            raise Exception("Неверный ввод.")
        if i == NUM_BORDER:
            is_number = not is_number
            if current_number:
                current_number = current_number[:len(current_number) - 1]
            if current_result == "":
                current_result = current_number
    if not current_number or not all([i in NUM_DIGITS for i in current_number]) or current_result.count(
            '.') > 1 or current_number.count('.') > 1:
        raise Exception("Неверный ввод.")
    else:
        if last_operation:
            current_result = balanced_ternary_operation(current_result, current_number, last_operation)
    return NUM_BORDER + current_result + NUM_BORDER
