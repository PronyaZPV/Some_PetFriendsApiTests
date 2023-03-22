import json
import pytest
import requests
from api import PetFriends
from settings import email, password, pet, pet2
from extensions import expect_all_keys, generate_string, russian_chars, chinese_chars, special_chars

pf = PetFriends()


@pytest.mark.get
@pytest.mark.negative
@pytest.mark.auth
def test_get_api_key_with_invalid_email(email='email', password=password):
    res, result = pf.get_api_key(email, password)
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'key' not in result, '*** Response must not contain a key ***'


@pytest.mark.get
@pytest.mark.negative
@pytest.mark.auth
def test_get_api_key_with_invalid_password(email=email, password='password'):
    res, result = pf.get_api_key(email, password)
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'key' not in result, '*** Response must not contain a key ***'


@pytest.mark.get
@pytest.mark.parametrize("filters",
                         ['', 'my_pets']
    , ids=['empty string', 'only my pets'])
def test_get_list_of_pets_with_valid_key(api_key, filters):
    if filters is None:
        filters = {}
    res, result = pf.get_list_of_pets(api_key, filters)
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result['pets']) > 0, '*** No list in response ***'
    expect_all_keys(result['pets'][0])  # функция для проверки наличия всех ключей в ответе


@pytest.mark.get
@pytest.mark.negative
@pytest.mark.parametrize("filters",
                         [generate_string(255),
                          generate_string(1001),
                          russian_chars(),
                          chinese_chars(),
                          special_chars(),
                          123
                          ],
                         ids=['255 symbols',
                              'more than 1000 symbols',
                              'russian',
                              'chinese',
                              'specials',
                              'digit'
                              ])
def test_get_list_of_pets_negative_with_valid_key(api_key, filters):
    if filters is None:
        filters = {}
    res, result = pf.get_list_of_pets(api_key, filters)
    assert res.status_code == 400, '*** Unexpected status-code, must be 200 ***'
    assert len(result['pets']) > 0, '*** No list in response ***'
    expect_all_keys(result['pets'][0])  # функция для проверки наличия всех ключей в ответе


@pytest.mark.get
@pytest.mark.negative
@pytest.mark.auth
def test_get_list_of_pets_with_invalid_key(filters=None):
    if filters is None:
        filters = {}
    auth_key = {'key': 'key123'}
    res, result = pf.get_list_of_pets(auth_key, filters)
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'pets' not in result, '*** Unexpected response ***'


@pytest.mark.post
def test_add_new_pet_with_valid_key(api_key):
    res, result = pf.add_new_pet(api_key, pet['name'], pet['age'], pet['animal_type'], pet['pet_photo'])
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    expect_all_keys(result)
    assert result.get('name') == pet['name'], '*** Unexpected name of pet ***'
    assert result.get('age') == pet['age'], '*** Unexpected age of pet ***'
    assert result.get('animal_type') == pet['animal_type'], '*** Unexpected animal_type of pet ***'


@pytest.mark.xfail(reason='Не реализована валидация полей')
@pytest.mark.post
@pytest.mark.negative
def test_add_new_pet_without_name(api_key):
    res, result = pf.add_new_pet(api_key, '', pet['age'], pet['animal_type'], pet['pet_photo'])
    assert res.status_code == 400, '*** Unexpected status-code, must be 400 ***'
    assert 'name' not in result, '*** Unexpected response ***'


@pytest.mark.post
@pytest.mark.negative
def test_add_new_pet_with_invalid_params(api_key):
    data = {'name': 'Cat'}
    headers = {'auth_key': api_key['key']}
    res = requests.post('https://petfriends.skillfactory.ru/api/pets', headers=headers, data=data)
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    assert res.status_code == 400, '*** Unexpected status-code, must be 400 ***'
    assert 'name' not in result, '*** Unexpected response ***'


@pytest.mark.post
@pytest.mark.negative
@pytest.mark.auth
def test_add_new_pet_with_invalid_key():
    auth_key = {'key': 'key123'}
    res, result = pf.add_new_pet(auth_key, pet['name'], pet['age'], pet['animal_type'], pet['pet_photo'])
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'

# Ниже тест не актуален из-за применения параметризации
# @pytest.mark.post
# def test_add_pet_simple_with_valid_key(api_key):
#     res, result = pf.add_pet_simple(api_key, pet['name'], pet['age'], pet['animal_type'])
#     assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
#     assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
#     expect_all_keys(result)
#     assert result.get('name') == pet['name'], '*** Unexpected name of pet ***'
#     assert result.get('age') == pet['age'], '*** Unexpected age of pet ***'
#     assert result.get('animal_type') == pet['animal_type'], '*** Unexpected animal_type of pet ***'
#     assert result.get('pet_photo') == "", '*** Unexpected pet_photo of pet ***'


@pytest.mark.parametrize("name",
                         [generate_string(255), generate_string(1001), russian_chars(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type",
                         [generate_string(255), generate_string(1001), russian_chars(), chinese_chars(),
                          special_chars(), '123'],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
@pytest.mark.post
def test_add_pet_simple_with_valid_key(api_key, name, animal_type, age):
    res, result = pf.add_pet_simple(api_key, name, age, animal_type)
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    # assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                         ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                          chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                              'int_max + 1', 'specials', 'russian', 'chinese'])
@pytest.mark.post
@pytest.mark.negative
def test_add_pet_simple_negative_with_valid_key(api_key, name, animal_type, age):
    res, result = pf.add_pet_simple(api_key, name, age, animal_type)
    assert res.status_code == 400, '*** Unexpected status-code, must be 400 ***'
    # assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    expect_all_keys(result)


@pytest.mark.post
@pytest.mark.negative
@pytest.mark.auth
def test_add_pet_simple_with_invalid_key():
    auth_key = {'key': 'key123'}
    res, result = pf.add_pet_simple(auth_key, pet['name'], pet['age'], pet['animal_type'])
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


@pytest.mark.post
def test_add_photo_of_pet_with_valid_key(api_key):
    pet_id = pf.get_pet_id(api_key, pet['name'], pet['age'], pet['animal_type'])
    res, result = pf.add_photo_of_pet(api_key, pet_id, pet['pet_photo'])
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    assert result.get('pet_photo').startswith('data:image/jpeg;base64,'), '*** Unexpected pet_photo of pet ***'
    expect_all_keys(result)


@pytest.mark.post
@pytest.mark.negative
@pytest.mark.auth
def test_add_photo_of_pet_with_invalid_key(api_key):
    pet_id = pf.get_pet_id(api_key, pet['name'], pet['age'], pet['animal_type'])
    auth_key = {'key': 'key123'}
    res, result = pf.add_photo_of_pet(auth_key, pet_id, pet['pet_photo'])
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


@pytest.mark.put
def test_update_information_about_pet_with_valid_key(api_key):
    pet_id = pf.get_pet_id(api_key, pet['name'], pet['age'], pet['animal_type'])
    res, result = pf.update_information_about_pet(api_key, pet_id, pet2['name'], pet2['age'], pet2['animal_type'])
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    assert result['name'] == pet2['name'], '*** Unexpected name of pet ***'
    assert result['age'] == pet2['age'], '*** Unexpected age of pet ***'
    assert result['animal_type'] == pet2['animal_type'], '*** Unexpected animal_type of pet ***'
    expect_all_keys(result)


@pytest.mark.delete
def test_delete_pet_with_valid_key(api_key):
    pet_id = pf.get_pet_id(api_key, pet['name'], pet['age'], pet['animal_type'])
    res, result = pf.delete_pet(api_key, pet_id)
    assert res.status_code == 200, '*** Unexpected status-code, must be 200 ***'
    assert 'name' not in result, '*** Unexpected response ***'


@pytest.mark.delete
@pytest.mark.negative
@pytest.mark.auth
def test_delete_pet_with_invalid_key():
    _, auth_key = pf.get_api_key(email, password)
    pet_id = pf.get_pet_id(auth_key, pet['name'], pet['age'], pet['animal_type'])
    auth_key = {'key': 'key123'}
    res, result = pf.delete_pet(auth_key, pet_id)
    assert res.status_code == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


@pytest.mark.skip(reason='Не тест. Используется для ручной чистки базы от тестовых питомцев')
def test_delete_all_test_pets(filters=None):
    """ Ручная чистка базы от созданных тестовых питомцев с указанным именем
        """
    if filters is None:
        filters = {}
    _, auth_key = pf.get_api_key(email, password)
    _, result = pf.get_list_of_pets(auth_key, filters)
    n = 0
    name_test_pet = 'Tasya'  # необходимо указать имя удаляемого питомца
    for i in result['pets']:
        if i['name'] == name_test_pet:
            n += 1
            pf.delete_pet(auth_key, i['id'])
    print(f'\nКоличество удалённых питомцев по имени {name_test_pet}:', n)
