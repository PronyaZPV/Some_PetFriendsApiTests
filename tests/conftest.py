import pytest
import requests
from api import PetFriends
from settings import base_url, email, password


@pytest.fixture(scope='session')
def api_key() -> dict:
    """ Сессионная фикстура - делает запрос к API сервера и возвращает результат в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и паролем.
        Далее передаёт в работу воспроизведение тестов (yield)
        После окончания тестов, удаляет тестовых питомцев.
        """
    headers = {
        'email': email,
        'password': password
    }
    res = requests.get(base_url + 'api/key', headers=headers)
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    assert 'key' in res.json(), '*** Response does not contain a key ***'
    # print('\nРезультат сессионной фикстуры: ', res.json())

    yield res.json()

    name_test_pet = ['Tasya', 'Tasya2', '']  # имена питомцев, создающиеся в автотестах
    n = 0
    _, result = PetFriends().get_list_of_pets(auth_key=res.json(), filters={})

    for pet in result['pets']:
        for name in name_test_pet:
            if pet['name'] == name:
                n += 1
                PetFriends().delete_pet(res.json(), pet['id'])
    print(f'\nКоличество удалённых записей:', n)
