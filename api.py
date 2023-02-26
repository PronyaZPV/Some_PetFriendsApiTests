import json
import requests
from requests_toolbelt import MultipartEncoder   # для загрузки изображений POST запросом


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> tuple[int, str | dict]:  # типы данных добавили для документации библиотеки
        """ Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
            с уникальным ключом пользователя, найденного по указанным email и паролем
            """
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        try:                      # если не выйдет перевести в json, то в текст
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: dict, filters: dict) -> tuple[int, str | dict]:
        """ Метод делает запрос к API сервера, возвращает статус запроса и результат в формате JSON
            со списком питомцев с учетом фильтров
            """
        headers = {'auth_key': auth_key['key']}
        filters = {'filter': filters}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filters)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: dict, name: str, age: str, animal_type: str, pet_photo: str) -> tuple[int, str | dict]:
        """ Метод делает запрос к API сервера, отправляя параметры питомца, создаёт питомца с фото,
            возвращает статус запроса и результат в формате JSON с параметрами нового питомца
            """
        # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        # при запуске из терминала могут быть проблемы с относительными путями
        # для избежания можно автоматом сделать полный путь
        data = MultipartEncoder(    # multipart-данные - смешанные json и файл
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)  # data - формат form data в теле запроса
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_simple(self, auth_key: dict, name: str, age: str, animal_type: str) -> tuple[int, str | dict]:
        """ Метод делает запрос к API сервера, отправляя параметры питомца, создаёт питомца без фото,
            возвращает статус запроса и результат в формате JSON с параметрами нового питомца
            """
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: dict, pet_id: str) -> tuple[int, str | dict]:
        """ Метод делает запрос к API сервера, удаляя питомца, и возвращает статус запроса и результат в формате JSON
            """
        headers = {'auth_key': auth_key['key']}
        pet_id = pet_id
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: dict, pet_id: str, pet_photo: str) -> tuple[int, str | dict]:
        """ Метод делает запрос к API сервера, добавляя фото питомцу,
            возвращает статус запроса и результат в формате JSON с параметрами питомца
            """
        pet_id = pet_id
        data = MultipartEncoder({
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_information_about_pet(self, auth_key: dict, pet_id: str,
                                     name: str = None, age: str = None,
                                     animal_type: str = None) -> tuple[int, str | dict]:
        """ Метод делает запрос к API сервера, заменяя параметры питомца без фото,
            возвращает статус запроса и результат в формате JSON с итоговыми параметрами питомца
            """
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_pet_id(self, auth_key: dict, name: str, age: str, animal_type: str) -> str:
        """ Внутренний метод для работы тестов - делает запрос к API сервера,
            отправляя параметры питомца, создаёт питомца без фото,
            возвращает id питомца в формате str
            """
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return result['id']