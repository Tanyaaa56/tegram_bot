from secret import BOT_TOKEN
import asyncio
import logging
import sys
from os import getenv
from keyboard import film_keyboard_markup, FilmCallback, menu_keyboard_markup, MenuCallback, keyboard_url
from data import get_films, add_film
from models import Film, FilmForm, MovieStates
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from commands import FILMS_BOT_COMMAND, FILMS_COMMAND, START_BOT_COMMAND, START_COMMAND

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv(BOT_TOKEN)

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

@dp.message(Command("guitar")) # /guitar Name guitar
async def guitar_info(message: Message, command: CommandObject):
    if command.args: # Name guitar
        guitar_name = command.args
        # guitars = get_guitar()
        # results = [film for film in films if query in film['genre'].lower()]
        # if results:
        #     for film in results:
        #         await message.answer(f"Знайдено: {html.bold(film['name'])} - {film['genre']}\n {film['description']}")
        # else:
        #     await message.answer("Фільм не знайдено.")
        await message.answer(guitar_name)
    else:
        await message.answer("Такої гітари немає")


@dp.message(CommandStart()) # /start
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {html.bold(message.from_user.full_name)}! \nЯ бот - помічник, для вибору фільма на вечір!", reply_markup=menu_keyboard_markup())

@dp.message(Command('video'))
async def command_video_handler(message: Message) -> None:
    await message.answer("Натисніть кнопку, щоб перейти за посиланням:",
                         reply_markup=keyboard_url('https://www.youtube.com/watch?v=kqtD5dpn9C8&ab_channel=ProgrammingwithMosh'))

@dp.callback_query(MenuCallback.filter())
async def menu1(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    await callback.message.answer('Був натиск на першу кнопку!')

@dp.message(Command('films')) # /films
async def command_film_handler(message: Message) -> None:
    films = get_films()
    markup = film_keyboard_markup(films)
    await message.answer(f'ТОП фільми 2024 🎬', reply_markup=markup)

@dp.callback_query(FilmCallback.filter())
async def callback_film(callback: CallbackQuery, callback_data:FilmCallback) -> None:
    film_id = callback_data.id # 0
    film_info = get_films(film_id=film_id)
    film = Film(**film_info)

    text = f"Фільм: {film.name}\n" \
           f"Опис: {film.description}\n" \
           f"Рейтинг: {film.rating}\n" \
           f"Жанр: {film.genre}\n" \
           f"Актори: {', '.join(film.actors)}\n"

    await callback.message.answer_photo(caption=text,
                                        photo=URLInputFile(film.poster))


@dp.message(Command('create_film')) # /create_film
async def create_film(message:Message, state:FSMContext) -> None:
    await state.set_state(FilmForm.name)
    await message.answer('Введіть назву фільму:', reply_markup=ReplyKeyboardRemove())

@dp.message(FilmForm.name)
async def create_name(message:Message, state:FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer('Введіть опис фільму одним абзацем:', reply_markup=ReplyKeyboardRemove())

@dp.message(FilmForm.description)
async def create_name(message:Message, state:FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer('Введіть рейтинг фільму(1-10):', reply_markup=ReplyKeyboardRemove())

@dp.message(FilmForm.rating)
async def create_name(message:Message, state:FSMContext) -> None:
    await state.update_data(rating=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer('Введіть жанр фільму:',reply_markup=ReplyKeyboardRemove())

@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer('Введіть перелік акторів фільму через роздільник ", "\n' + html.bold("Обов\'язкова кома та відступ після неї."), reply_markup=ReplyKeyboardRemove())

@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
   await state.update_data(actors=[x for x in message.text.split(", ")])
   await state.set_state(FilmForm.poster)
   await message.answer(
       f"Введіть посилання на постер фільму.",
       reply_markup=ReplyKeyboardRemove())

@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
   data = await state.update_data(poster=message.text)
   film = Film(**data)
   add_film(film.model_dump())
   await state.clear()
   await message.answer(
       f"Фільм {film.name} успішно додано!",
       reply_markup=ReplyKeyboardRemove(),
   )


@dp.message(Command('search_film'))
async def search_movie(message: Message, state: FSMContext):
    await message.answer("Введіть назву фільму для пошуку:")
    await state.set_state(MovieStates.search_query)


@dp.message(MovieStates.search_query)
async def get_search_query(message: Message, state: FSMContext):
    query = message.text.lower()
    films = get_films()
    results = [film for film in films if query in film['name'].lower()]
    if results:
        for film in results:
            await message.answer(f"Знайдено: {html.bold(film['name'])} \n {film['description']}")
    else:
        await message.answer("Фільм не знайдено.")
    await state.clear()


@dp.message(Command('filter_film_by_genre'))
async def filter_movie_genre(message: Message, state: FSMContext):
    await message.answer("Введіть жанр фільму для пошуку:")
    await state.set_state(MovieStates.filter_criteria)


@dp.message(MovieStates.filter_criteria)
async def get_search_query(message: Message, state: FSMContext):
    query = message.text.lower()
    films = get_films()
    results = [film for film in films if query in film['genre'].lower()]
    if results:
        for film in results:
            await message.answer(f"Знайдено: {html.bold(film['name'])} - {film['genre']}\n {film['description']}")
    else:
        await message.answer("Фільм не знайдено.")
    await state.clear()


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         # Send a copy of the received message
#         await message.answer(f'Твоє повідомлення: ')
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([START_BOT_COMMAND,FILMS_BOT_COMMAND])
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())