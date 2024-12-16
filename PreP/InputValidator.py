import re


def npn_checker(val):
    pattern = r'^([1-9]\d*|)$'
    return re.match(pattern, val) is not None


def rpn_checker(val):
    pattern = r'^(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def rn_checker(val):
    pattern = r'^-?(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None