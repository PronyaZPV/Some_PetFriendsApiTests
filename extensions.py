def expect_all_keys(result: dict):
    ''' Функция для проверки наличия всех ключей в ответе.
        На вход получает json с параметрами питомца.
        На выходе результат команды assert
        '''
    assert 'name' in result, '*** Missing key "name" ***'
    assert 'age' in result, '*** Missing key "age" ***'
    assert 'animal_type' in result, '*** Missing key "animal_type" ***'
    assert 'pet_photo' in result, '*** Missing key "pet_photo" ***'
    assert 'created_at' in result, '*** Missing key "created_at" ***'
    assert 'id' in result, '*** Missing key "id" ***'
    assert 'user_id' in result, '*** Missing key "user_id" ***'
    return