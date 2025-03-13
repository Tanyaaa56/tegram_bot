from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class FilmCallback(CallbackData, prefix='film', sep=';'):
    id: int
    name: str


def film_keyboard_markup(films_list:list[dict], offset:int|None=None,
                         skip:int|None=None):
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)
    for index, film_data in enumerate(films_list):
        callback_data = FilmCallback(id=index, **film_data)
        builder.button(text=f"{callback_data.name}", callback_data=callback_data.pack())
    builder.adjust(1, repeat=True)
    return builder.as_markup()


class MenuCallback(CallbackData, prefix='part', sep='_'):
    id: int
def menu_keyboard_markup():
    builder = InlineKeyboardBuilder()
    builder.button(text='Розділ_1', callback_data=MenuCallback(id=1))
    builder.button(text='Розділ_2', callback_data=MenuCallback(id=2))
    builder.button(text='Розділ_3', callback_data=MenuCallback(id=3))
    return builder.as_markup()


def keyboard_url(url):
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти за посиланням", url=str(url))
    return builder.as_markup()
