import requests
import requests_mock
import unittest

def get_hero_by_id(hero_id):
    url = f'https://akabab.github.io/superhero-api/api/id/{hero_id}.json'
    response = requests.get(url)
    
    if response.status_code == 404:
        print(f"Hero with ID {hero_id} not found.")
        return None
    
    response.raise_for_status()  # Выбрасывает исключение при ошибке запроса
    return response.json()

if __name__ == "__main__":  # Проверка нашего героя/
    hero_id_input = int(input("Enter the superhero ID: "))  # Ввод ID супергероя
    hero_data = get_hero_by_id(hero_id_input)
    if hero_data:
        print("Hero Data:")
        print(f"ID: {hero_data['id']}")
        print(f"Name: {hero_data['name']}")

# Тесты
class TestGetHeroById(unittest.TestCase):

    def test_valid_hero_id(self):  # Тест на вызов минимального ID
        hero_data = get_hero_by_id(1)
        self.assertIsNotNone(hero_data)
        self.assertEqual(hero_data['id'], 1)

    def test_invalid_hero_id(self):  # Тест на несуществующий ID
        hero_data = get_hero_by_id(9999)
        self.assertIsNone(hero_data, "Expected None for invalid ID")

    def test_negative_hero_id(self):  # Тест на неверный ID
        hero_data = get_hero_by_id(-1)
        self.assertIsNone(hero_data, "Expected None for negative ID")

    def test_success_status_code(self):
        response = requests.get('https://akabab.github.io/superhero-api/api/id/1.json')
        self.assertEqual(response.status_code, 200)

    def test_missing_field(self):  # Тест на отсутствие обязательных полей
        hero_data = {
            'id': 1,
            # Пропущено поле 'name'
            'powerstats': {'intelligence': 100}
        }
        self.assertNotIn('name', hero_data)

    def test_invalid_data_type(self):  # Тест на различные типы данных внутри полей
        hero_data = {
            'id': 1,
            'powerstats': {'intelligence': 'high'}  # Ожидали число, получили строку
        }
        self.assertIsInstance(hero_data['powerstats']['intelligence'], str)

    def test_partial_response(self):
        partial_data = {
            'id': 1,
            # Пропущены некоторые ключи: 'appearance', 'biography'
            'powerstats': {'intelligence': 100}
        }
        self.assertIn('id', partial_data)
        self.assertNotIn('appearance', partial_data)

    def test_large_id(self):  # Тест на максимальный ID
        hero_data = get_hero_by_id(731)  
        self.assertIsNotNone(hero_data)

    def test_empty_response(self):  # Тест на пустой JSON ответ
        with requests_mock.Mocker() as mocker:
            mocker.get('https://akabab.github.io/superhero-api/api/id/1.json', json={})
            hero_data = get_hero_by_id(1)
            self.assertEqual(hero_data, {}, "Expected an empty dictionary for empty response")


    def test_invalid_url(self):  # Тест на несуществующий URL
        with requests_mock.Mocker() as mocker:
            mocker.get('https://akabab.github.io/superhero-api/api/id/9999999.json', status_code=404)
            hero_data = get_hero_by_id(9999999)
            self.assertIsNone(hero_data)

    def test_unexpected_data_format(self):  # Тест на неожиданный формат данных
        with requests_mock.Mocker() as mocker:
            mocker.get('https://akabab.github.io/superhero-api/api/id/1.json', text="<html>Not Found</html>")
            with self.assertRaises(ValueError):
                get_hero_by_id(1)

    def test_http_error_handling(self):  # Тест на обработку HTTP ошибок
        with requests_mock.Mocker() as mocker:
            mocker.get('https://akabab.github.io/superhero-api/api/id/1.json', status_code=500)
            with self.assertRaises(requests.exceptions.HTTPError):
                get_hero_by_id(1)

    def test_hero_data_keys(self):  # Тест на наличие всех основных ключей в ответе
        hero_data = get_hero_by_id(1)
        expected_keys = ['id', 'name', 'powerstats', 'appearance', 'biography']
        for key in expected_keys:
            self.assertIn(key, hero_data)

if __name__ == '__main__':
    unittest.main()
