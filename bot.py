import os
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from googletrans import Translator
from gtts import gTTS

# Токен вашего Telegram-бота
TELEGRAM_TOKEN = "8194842561:AAF5oFweiTJCnMCc8-L33Ad3ciPaXbmvFOQ"

# Инициализация бота, диспетчера и роутера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Создание папки для сохранения фото
if not os.path.exists("img"):
    os.makedirs("img")

# Переводчик
translator = Translator()

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот, который умеет сохранять фотографии, переводить текст и отправлять голосовые сообщения.")

# Обработчик команды /help
@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Я могу:\n"
        "- Сохранять отправленные фотографии.\n"
        "- Переводить текст на английский язык.\n"
        "- Отправлять голосовые сообщения.\n\n"
        "Просто отправь фото или текст!"
    )

# Обработчик получения фото
@router.message(lambda message: message.content_type == ContentType.PHOTO)
async def save_photo(message: Message):
    # Получаем файл
    photo = message.photo[-1]  # Берём фото с наибольшим разрешением
    file = await bot.get_file(photo.file_id)

    # Сохраняем фото
    file_name = f"img/{photo.file_id}.jpg"
    await bot.download_file(file.file_path, file_name)

    await message.answer("Фото сохранено!")

# Обработчик текста для перевода
@router.message(lambda message: message.content_type == ContentType.TEXT)
async def translate_text(message: Message):
    # Перевод текста
    translated = translator.translate(message.text, src="auto", dest="en")
    await message.answer(f"Перевод:\n{translated.text}")

# Обработчик команды /voice
@router.message(Command("voice"))
async def send_voice_message(message: Message):
    # Генерируем голосовое сообщение
    text = "Привет! Это тестовое голосовое сообщение."
    tts = gTTS(text, lang="ru")
    tts.save("voice.mp3")

    # Отправляем голосовое сообщение
    with open("voice.mp3", "rb") as voice_file:
        await message.answer_voice(voice_file)

# Основная функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())