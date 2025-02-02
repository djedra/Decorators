import os
from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        data_function = []
        keywords = ['Текущее время и дата', 'Имя функции', 'Аргументы вызова функции',
                    'Возвращаемое значение функции']
        date = datetime.now()
        date_string = date.strftime('%m/%d/%y %H:%M:%S')
        data_function.append(date_string)
        function_name = old_function.__name__
        data_function.append(function_name)
        if args and kwargs:
            arguments = [list(args), kwargs]
            data_function.append(arguments)
        elif args:
            data_function.append(list(args))
        elif kwargs:
            data_function.append(kwargs)
        result = old_function(*args, **kwargs)
        data_function.append(result)
        data = dict(zip(keywords, data_function))
        with open('main.log', 'a', encoding='utf8') as f:
            f.write(f'{str(data)}\n')
        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path, encoding='utf8') as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'
