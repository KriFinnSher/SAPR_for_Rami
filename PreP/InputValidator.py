import re
from tkinter import messagebox


def npn_checker(val):
    pattern = r'^([1-9]\d*|)$'
    return re.match(pattern, val) is not None


def rpn_checker(val):
    pattern = r'^(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def rn_checker(val):
    pattern = r'^-?(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def tcoi(input_data):
    for key, values in list(input_data.items())[:-1]:
        if any(val == '' for val in values):
            messagebox.showerror('Ошибка', 'Присутствуют пустые поля ввода')
            return False

    e, a, l = input_data['E'], input_data['A'], input_data['L']

    for eal in zip(e, a, l):
        if float(eal[0]) * float(eal[1]) * float(eal[2]) == 0:
            messagebox.showerror('Ошибка', 'Одно из полей [E, A, L] имеет нулевое значение')
            return False

    return True