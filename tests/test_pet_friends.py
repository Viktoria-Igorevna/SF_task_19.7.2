from api import PetFriends
from settings import valid_email, valid_password, animal_age_1, animal_foto_1, animal_name_1, \
    animal_types_1, animal_name_update, animal_age_2, animal_types_2, animal_name_2, animal_foto_2, \
    not_valid_email, not_valid_password

pf = PetFriends()

# Тест на получение ключа и статуса 200 с валидными email и паролем
def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# Тест на получение списка животного и статуса 200 с валидным ключом
def test_get_list_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# Тест на создание нового питомца и статуса 200 с валидными ключом и значениями в параметрах питомца
def test_add_new_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, animal_name_1, animal_types_1, animal_age_1, animal_foto_1)
    assert status == 200
    assert 'id' in result

# Тест на создание нового питомца без фотографии и статуса 200 с валидными ключом и значениями в параметрах питомца
def test_add_new_pet_without_photo_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, animal_name_2, animal_types_2, animal_age_2)
    assert status == 200
    assert 'id' in result

# Тест на удаление питомца и статуса 200 с валидными ключом и id
def test_del_pet_with_valid_key_and_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    animal_id = pf.search_pet(auth_key, animal_name_3)
    _, data = pf.get_list_pets(auth_key, 'my_pets')
    count_animal_before = len(data['pets'])
    status = pf.del_pet(auth_key, animal_id)
    _, data = pf.get_list_pets(auth_key, 'my_pets')
    count_animal_after = len(data['pets'])
    assert status == 200
    assert count_animal_before == count_animal_after + 1
    assert animal_id not in data['pets']

# Тест на изменение питомца и статуса 200 с валидными ключом и значениями в параметрах питомца
def test_update_pet_with_valid_key_and_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    animal_id = pf.search_pet(auth_key, animal_name_2)
    status, result = pf.update_pet(auth_key, animal_id, animal_name_update, animal_types_2, animal_age_2)
    assert status == 200
    assert animal_name_update == result['name']

# Тест на добавление фотографии к питомцу и статуса 200 с валидными ключом и фотографией
def test_add_photo_of_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    animal_id = pf.search_pet(auth_key, animal_name_2)
    status, result = pf.add_photo_of_pet(auth_key, animal_id, animal_foto_2)
    assert status == 200
    assert result['pet_photo'] != ''

# Тест на получение списка моих животных и статуса 200 с валидным ключом
def test_get_list_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# Тест на получение ключа с не валидным email
def test_get_api_key_for_not_valid_user(email = not_valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

# Тест на получение ключа с не валидными паролем
def test_get_api_key_for_not_valid_password(email = valid_email, password = not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

# Тест на добавление фотографии к питомцу, но вместо фотографии используется текстовый файл
def test_add_not_valid_photo_of_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    animal_id = pf.search_pet(auth_key, animal_name_2)
    status, result = pf.add_photo_of_pet(auth_key, animal_id, 'images/cat.txt')
    assert status == 500



# Негативные тесты, которые показывают БАГИ

# Тест на создание нового питомца без фотографии с отрицательным числом в возрасте
def test_add_new_pet_without_photo_with_not_valid_age_1():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, animal_name_2, animal_types_2, -60)
    assert status == 400

# Тест на создание нового питомца без фотографии со строкой в возрасте
def test_add_new_pet_without_photo_with_not_valid_age_2():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, animal_name_2, animal_types_2, 'hhh')
    assert status == 400

# Тест на создание нового питомца без фотографии с числом в имени
def test_add_new_pet_without_photo_with_with_not_valid_name():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, animal_name_2, animal_types_2, -60)
    assert status == 400

