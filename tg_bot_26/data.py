import json

def get_guitar(file_path:str = "music.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_info = json.load(f)
        all_instruments = []
        for guitarist in all_info:
            for i in guitarist['instruments']:
                all_instruments.append(i)
        return all_instruments



def get_films(file_path:str = "films.json", film_id:int|None = None) -> list[dict]|dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        films = json.load(f)
        if not film_id is None and film_id < len(films):
            return films[film_id]
        return films

def add_film(film:dict, file_path:str = "films.json"):
    films = get_films()
    if film:
        films.append(film)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(films, f, indent=4, ensure_ascii=False)