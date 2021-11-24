
RED = '\033[31m'  # 红色
GREEN = '\033[32m'  # 绿色
YELLOW = '\033[33m'  # 黄色
BLUE = '\033[34m'  # 蓝色
FUCHSIA = '\033[35m'  # 紫红色
CYAN = '\033[36m'  # 青蓝色
WHITE = '\033[37m'  # 白色

RESET = '\033[0m'  # 终端默认颜色


def color_str(color, s):
    return '{}{}'.format(color, s)


def normal(s):
    return color_str(RESET, s)


def red(s):
    return color_str(RED, s)


def green(s):
    return color_str(GREEN, s)


def yellow(s):
    return color_str(YELLOW, s)


def blue(s):
    return color_str(BLUE, s)


def fuchsia(s):
    return color_str(FUCHSIA, s)


def cyan(s):
    return color_str(CYAN, s)


def white(self, s):
    return color_str(WHITE, s)


if '__main__' == __name__:
    print(red(123))
