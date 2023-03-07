import datetime


def expect_all_keys(res: dict) -> object:
    """ Функция для проверки наличия всех ключей в ответе.
        На вход получает json с параметрами питомца.
        На выходе результат команды assert
        """
    assert 'name' in res, '*** Missing key "name" ***'
    assert 'age' in res, '*** Missing key "age" ***'
    assert 'animal_type' in res, '*** Missing key "animal_type" ***'
    assert 'pet_photo' in res, '*** Missing key "pet_photo" ***'
    assert 'created_at' in res, '*** Missing key "created_at" ***'
    assert 'id' in res, '*** Missing key "id" ***'
    assert 'user_id' in res, '*** Missing key "user_id" ***'
    return


def logger(func):
    """ Декоратор для логирование работы функций, возвращающих объект response.
        Результат работы записывается в файл log.txt
        """
    def wrapper(*args, **kwargs):
        res_func = func(*args, **kwargs)
        res, _ = res_func
        with open('log.txt', 'a') as inf:
            inf.write(f'{datetime.datetime.now()} | Test: {func.__name__}'
                      f'\nMethod = {res.request.method}'
                      f'\nURL = {res.request.url}'
                      f'\nPath_URL = {res.request.path_url}'
                      f'\nRequest headers = {res.request.headers}'
                      f'\nRequest body = {res.request.body}'
                      f'\n\nStatus_code = {res.status_code}'
                      f'\nResponse body = {res.text.split(",/9j/")[0]}'  # намеренно обрезал body, чтобы не было огромной "портянки"
                      f'\n{"-" * 40}\n')
        return res_func
    return wrapper
