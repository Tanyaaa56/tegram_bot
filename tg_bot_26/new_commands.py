from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from secret import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/phone")
async def request_phone(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Надіслати номер телефону", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Будь ласка, надішліть свій номер телефону:", reply_markup=keyboard)

@dp.message(F.contact)
async def handle_phone(message: types.Message):
    phone_number = message.contact.phone_number
    await message.answer(f"Дякую! Ваш номер телефону: {phone_number}")

@dp.message(F.text == "/location")
async def request_location(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Надіслати геолокацію", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Будь ласка, надішліть свою геолокацію:", reply_markup=keyboard)

@dp.message(F.location)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await message.answer(f"Дякую! Ваша геолокація:\nШирота: {latitude}\nДовгота: {longitude}")

@dp.message(F.text == "/photo")
async def send_photo(message: types.Message):
    photo_url = "https://example.com/image.jpg"  # Замініть на своє зображення
    await message.answer_photo(photo=photo_url, caption="Ось ваше фото! 📸")

@dp.message(F.text == "/video")
async def send_video(message: types.Message):
    video_url = "https://www.youtube.com/watch?v=kqtD5dpn9C8&ab_channel=ProgrammingwithMosh"  # Замініть на своє відео
    await message.answer_video(video=video_url, caption="Ось ваше відео! 🎥")

@dp.message(F.text == "/gif")
async def send_gif(message: types.Message):
    gif_url = "https://no-cdn.shortpixel.ai/client/to_avif,q_lossy,ret_wait/https://shortpixel.com/blog/wp-content/uploads/2023/12/nyan-cat.gif"  # Замініть на свій GIF
    await message.answer_animation(animation=gif_url, caption="Ось ваш GIF! 🎞️")

@dp.message(F.text == "/document")
async def send_document(message: types.Message):
    doc_url = "https://example.com/file.pdf"  # Замініть на свій файл
    await message.answer_document(document=doc_url, caption="Ось ваш документ 📄")

@dp.message(F.text == "/voice")
async def send_voice(message: types.Message):
    voice_url = "https://example.com/audio.ogg"  # Замініть на свій голосовий файл
    await message.answer_voice(voice=voice_url, caption="Ось ваше голосове повідомлення 🎙️")

@dp.message(F.text == "/audio")
async def send_audio(message: types.Message):
    audio_url = "https://example.com/audio.mp3"  # Замініть на свій файл
    await message.answer_audio(audio=audio_url, caption="Ось ваша аудіозапис 🎵")

@dp.message(F.text == "/sticker")
async def send_sticker(message: types.Message):
    sticker_id = "CAACAgIAAxkBAAEFgV1lKmj..."  # Замініть на ID стікера
    await message.answer_sticker(sticker=sticker_id)

@dp.message(F.text == "/poll")
async def send_poll(message: types.Message):
    await message.answer_poll(
        question="Що вам більше подобається?",
        options=["Чай", "Кава", "Сік"],
        is_anonymous=False  # Опитування не анонімне
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
