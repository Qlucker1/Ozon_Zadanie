import requests

def get_heroes():
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)
    response.raise_for_status()  # Выбрасывает исключение при ошибке запроса
    return response.json()

def find_tallest_hero(gender, has_work):
    heroes = get_heroes()
    
    # Фильтруем героев по полу и наличию работы
    filtered_heroes = [
        hero for hero in heroes 
        if hero['appearance']['gender'] == gender and 
        bool(hero.get('work', {}).get('occupation')) == has_work
    ]
    
    # Находим самого высокого героя в строковом формате/
    tallest_hero = max(
        filtered_heroes,
        key=lambda hero: hero['appearance']['height'][1],  # Высота остается в строковом формате
        default=None
    )

    return (tallest_hero['id'], tallest_hero['name'], tallest_hero['appearance']['height'][1]) if tallest_hero else (None, None, None)

if __name__ == "__main__":
    gender_input = 'Female'  # Замените на нужный пол
    has_work_input = True  # Замените на нужное булевое значение
    tallest_hero_id, tallest_hero_name, height = find_tallest_hero(gender=gender_input, has_work=has_work_input)

    if tallest_hero_name:
        print(f"The tallest hero is {tallest_hero_name} (ID: {tallest_hero_id}) with a height of {height}.")  # Высота в строковом формате
    else:
        print("No hero found matching the criteria.")
