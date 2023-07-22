import requests
import json

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(f'{self.base_url}/api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def get_list_pets(self, auth_key, filter: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""
        headers = {'auth_key': auth_key['key']}

        res = requests.get(f'{self.base_url}/api/pets?filter={filter}', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_foto: str) -> json:
        """ Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        c добавленным новым животным с указанными ключом, именем, типом живого, возраста и названием
        фотографии"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_foto, open(pet_foto, 'rb'), 'image/jpeg')}

        res = requests.post(f'{self.base_url}/api/pets', headers=headers, data=data, files=file)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def search_pet(self, auth_key: json, name: str) -> str:
        """Метод возвращает id животного с именем name в списке 'мои животные'"""
        _, my_animals = PetFriends.get_list_pets(self, auth_key, 'my_pets')
        id = ''
        for pet in my_animals['pets']:
            if name == pet['name']:
                id = pet['id']
                break
        return id

    def del_pet(self, auth_key: json, pet_id: str) -> int:
        """Метод делает запрос к API сервера и возвращает статус запроса, после удаления животного
        в списке 'мои животные'"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(f'{self.base_url}/api/pets/{pet_id}', headers=headers)

        status = res.status_code
        return status

    def update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
                возвращает статус запроса и result в формате JSON с обновлённый данными питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(f'{self.base_url}/api/pets/{pet_id}', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """ Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        c добавленным новым животным с указанными ключом, именем, типом живого, возраста """

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(f'{self.base_url}/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_foto: str):
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_foto, open(pet_foto, 'rb'), 'image/jpeg')}
        res = requests.post(f'{self.base_url}/api/pets/set_photo/{pet_id}', headers=headers, files=file)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result







