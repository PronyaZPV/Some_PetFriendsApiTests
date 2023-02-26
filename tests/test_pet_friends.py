import json
import requests
from api import PetFriends
from settings import email, password, pet, pet2
from extensions import expect_all_keys

pf = PetFriends()


def test_get_api_key_with_valid_user(email=email, password=password):
    status, result = pf.get_api_key(email, password)
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert 'key' in result, '*** Response does not contain a key ***'


def test_get_api_key_with_invalid_email(email='email', password=password):
    status, result = pf.get_api_key(email, password)
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'key' not in result, '*** Response must not contain a key ***'


def test_get_api_key_with_invalid_password(email=email, password='password'):
    status, result = pf.get_api_key(email, password)
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'key' not in result, '*** Response must not contain a key ***'


def test_get_list_of_pets_with_valid_key(filters=None):
    if filters is None:
        filters = {}
    _, auth_key = pf.get_api_key(email, password)  # _ - это status, он не нужен, поэтому "_"
    status, result = pf.get_list_of_pets(auth_key, filters)
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result['pets']) > 0, '*** No list in response ***'
    expect_all_keys(result['pets'][0])  # функция для проверки наличия всех ключей в ответе


def test_get_list_of_pets_with_invalid_key(filters=None):
    if filters is None:
        filters = {}
    auth_key = {'key': 'key123'}
    status, result = pf.get_list_of_pets(auth_key, filters)
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'pets' not in result, '*** Unexpected response ***'


def test_add_new_pet_with_valid_key():
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.add_new_pet(auth_key, pet['name'], pet['age'], pet['animal_type'], pet['pet_photo'])
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    expect_all_keys(result)
    assert result.get('name') == pet['name'], '*** Unexpected name of pet ***'
    assert result.get('age') == pet['age'], '*** Unexpected age of pet ***'
    assert result.get('animal_type') == pet['animal_type'], '*** Unexpected animal_type of pet ***'


def test_add_new_pet_without_name():
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.add_new_pet(auth_key, '', pet['age'], pet['animal_type'], pet['pet_photo'])
    assert status == 400, '*** Unexpected status-code, must be 400 ***'
    assert 'name' not in result, '*** Unexpected response ***'


def test_add_new_pet_with_invalid_params():
    _, auth_key = pf.get_api_key(email, password)
    data = {'name': 'Cat'}
    headers = {'auth_key': auth_key['key']}

    res = requests.post('https://petfriends.skillfactory.ru/api/pets', headers=headers, data=data)
    status = res.status_code
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text

    assert status == 400, '*** Unexpected status-code, must be 400 ***'
    assert 'name' not in result, '*** Unexpected response ***'


def test_add_new_pet_with_invalid_key():
    auth_key = {'key': 'key123'}
    status, result = pf.add_new_pet(auth_key, pet['name'], pet['age'], pet['animal_type'], pet['pet_photo'])
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


def test_add_pet_simple_with_valid_key():
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.add_pet_simple(auth_key, pet['name'], pet['age'], pet['animal_type'])
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    expect_all_keys(result)
    assert result.get('name') == pet['name'], '*** Unexpected name of pet ***'
    assert result.get('age') == pet['age'], '*** Unexpected age of pet ***'
    assert result.get('animal_type') == pet['animal_type'], '*** Unexpected animal_type of pet ***'
    assert result.get('pet_photo') == "", '*** Unexpected pet_photo of pet ***'


def test_add_pet_simple_with_invalid_key():
    auth_key = {'key': 'key123'}
    status, result = pf.add_pet_simple(auth_key, pet['name'], pet['age'], pet['animal_type'])
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


def test_add_photo_of_pet_with_valid_key():
    _, auth_key = pf.get_api_key(email, password)
    pet_id = pf.get_pet_id(auth_key, pet['name'], pet['age'], pet['animal_type'])
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet['pet_photo'])
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    assert result.get('pet_photo').startswith('data:image/jpeg;base64,'), '*** Unexpected pet_photo of pet ***'
    expect_all_keys(result)


def test_add_photo_of_pet_with_invalid_key():
    _, auth_key = pf.get_api_key(email, password)
    pet_id = pf.get_pet_id(auth_key, pet['name'], pet['age'], pet['animal_type'])
    auth_key = {'key': 'key123'}
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet['pet_photo'])
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


def test_update_information_about_pet_with_valid_key():
    _, auth_key = pf.get_api_key(email, password)
    pet_id = pf.get_pet_id(auth_key, pet['name'], pet['age'], pet['animal_type'])
    status, result = pf.update_information_about_pet(auth_key, pet_id, pet2['name'], pet2['age'], pet2['animal_type'])
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert len(result) == 7, '*** Unexpected number of parameters in the response ***'
    assert result['name'] == pet2['name'], '*** Unexpected name of pet ***'
    assert result['age'] == pet2['age'], '*** Unexpected age of pet ***'
    assert result['animal_type'] == pet2['animal_type'], '*** Unexpected animal_type of pet ***'
    expect_all_keys(result)


def test_delete_pet_with_valid_key():
    _, auth_key = pf.get_api_key(email, password)
    pet_id = pf.get_pet_id(auth_key, pet['name'], pet['age'], pet['animal_type'])
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200, '*** Unexpected status-code, must be 200 ***'
    assert 'name' not in result, '*** Unexpected response ***'


def test_delete_pet_with_invalid_key():
    _, auth_key = pf.get_api_key(email, password)
    pet_id = pf.get_pet_id(auth_key, pet['name'], pet['age'], pet['animal_type'])
    auth_key = {'key': 'key123'}
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 403, '*** Unexpected status-code, must be 403 ***'
    assert 'name' not in result, '*** Unexpected response ***'


# def test_delete_all_test_pets(filters={}):
#     """ Подчистить базу от созданных тестовых питомцев с указанным именем
#         """
#
#     _, auth_key = pf.get_api_key(email, password)
#     _, result = pf.get_list_of_pets(auth_key, filters)
#     n = 0
#     name_test_pet = 'Tasya'   # необходимо указать имя удаляемого питомца
#     for i in result['pets']:
#         if i['name'] == name_test_pet:
#             n += 1
#             pf.delete_pet(auth_key, i['id'])
#     print(f'\nКоличество удалённых кошек по имени {name_test_pet}:', n)










    ''' Пример проверки, что список питомцев не пустой, иначе
        проброс ошибки в консоль
        '''

    # def test_successful_update_self_pet_info(self, name='Мурзик',
    #                                          animal_type='Котэ', age=5):
    #     _, auth_key = self.pf.get_api_key(valid_email, valid_password)
    #     _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")
    #
    #     if len(my_pets['pets']) > 0:
    #         status, result = self.pf.update_pet_info(auth_key, my_pets['pets'][0]['id'],
    #                                                  name, animal_type, age)
    #         assert status == 200
    #         assert result['name'] == name
    #     else:
    #         raise Exception("There is no my pets")
