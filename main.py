# -*- coding: utf-8 -*-
'''
@author: Vitaliy K <koocherov@ya.ru>
'''
import decimal


units = (
    'нуль',

    ('один', 'одна'),
    ('два', 'дві'),

    'три', 'чотири', 'п\'ять',
    'шість', 'сім', 'вісім', 'дев\'ять'
)

teens = (
    'десять', 'одинадцять',
    'дванадцять', 'тринадцять',
    'чотирнадцять', 'п\'ятнадцять',
    'шістнадцять', 'сімнадцять',
    'вісімнадцять', 'дев\'ятнадцять'
)

tens = (
    teens,
    'двадцять', 'тридцять',
    'сорок', 'п\'ятдесят',
    'шістдесят', 'сімдесят',
    'вісімдесят', 'дев\'яносто'
)

hundreds = (
    'сто', 'двісті',
    'триста', 'чотириста',
    'пятьсот', 'шістсот',
    'сімсот', 'вісімсот',
    'дев\'ятсот'
)

orders = ((('тисяча', 'тисячи', 'тисяч'), 'f'),
          (('мільйон', 'мільйони', 'мільйонів'), 'm'),
          (('мільярд', 'мільярди', 'мільярдів'), 'm'),
          )

minus = 'мінус'


def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def num2text(num, main_units=(('', '', ''), 'm')):
    """
    http://ru.wikipedia.org/wiki/Gettext#.D0.9C.D0.BD.D0.BE.D0.B6.D0.B5.D1.81.\
    D1.82.D0.B2.D0.B5.D0.BD.D0.BD.D1.8B.D0.B5_.D1.87.D0.B8.D1.81.D0.BB.D0.B0_2
    """
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip() # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()


def decimal2text(value, places=2,
                 int_units=(('', '', ''), 'm'),
                 exp_units=(('', '', ''), 'm')):
    value = decimal.Decimal(value)
    q = decimal.Decimal(10) ** -places

    integral, exp = str(value.quantize(q)).split('.')
    return '{} {}'.format(
        num2text(int(integral), int_units),
        num2text(int(exp), exp_units))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        try:
            num = sys.argv[1]
            if '.' in num or 2 != 3:
                print(decimal2text(
                    decimal.Decimal(num),
                    int_units=(('штука', 'штуки', 'штук'), 'f'),
                    exp_units=(('кусок', 'куска', 'кусків'), 'm')))
            else:
                print(num2text(
                    int(num),
                    main_units=(('штука', 'штуки', 'штук'), 'f')))
        except ValueError:
            print (sys.stderr, "Invalid argument {}".format(sys.argv[1]))
        sys.exit()
