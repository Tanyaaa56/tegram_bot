from pydantic import BaseModel
from aiogram.fsm.state import State, StatesGroup

class Film(BaseModel):
    name: str
    description: str
    rating: float
    genre: str
    actors: list[str]
    poster: str

class FilmForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()

class MovieStates(StatesGroup):
    search_query = State()
    filter_criteria = State()
    delete_query = State()
    edit_query = State()
    edit_description = State()