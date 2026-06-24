import os
import datetime
from functools import wraps


def logger(path):
    """Параметризованный декоратор для логирования в указанный файл."""

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            # 1. Формируем временную метку
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 2. Готовим базовое сообщение
            log_message = f"[{timestamp}] Вызов функции: {old_function.__name__}\n"
            log_message += f"Аргументы: args={args}, kwargs={kwargs}\n"

            try:
                # 3. Выполняем функцию
                result = old_function(*args, **kwargs)
                log_message += f"Возвращаемое значение: {result}\n"
            except Exception as e:
                # 4. Логируем ошибку и пробрасываем исключение
                log_message += f"Возникшая ошибка: {type(e).__name__}: {e}\n"
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(log_message)
                raise

            # 5. Если ошибок не было, записываем лог в файл
            with open(path, 'a', encoding='utf-8') as f:
                f.write(log_message)

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path, encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()