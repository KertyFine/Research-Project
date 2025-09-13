import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

BOT_TOKEN = "8441758015:AAEtvt2O91_t7ft1N-WU9FnLt-9IyS7YnoY"

logging.basicConfig(level = logging.INFO)

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

kb_builder = ReplyKeyboardBuilder()
kb_builder.add(KeyboardButton(text = "Составить маршрут"), KeyboardButton(text = "Информация о месте"))
kb_builder.adjust(2)
reply_kb = kb_builder.as_markup(resize_keyboard = True)

class GetPreferences(StatesGroup):
    location = State()
    budget = State()
    duration = State()
    interests = State()
    transport = State()

@dp.message(Command("start"))
async def cmd_start(message : types.Message, state : FSMContext):
    await message.answer("Привет! Я бот для генераци маршрутов по Беларуси.\nДавайте сначала определим ваши предпочтения.\nВведите желаемую местность или город", reply_markup = reply_kb)
    #await state.set_state(GetPreferences.location)

@dp.message()
async def start_getting_preferences(message : types.Message, state : FSMContext):
    if message.text.lower() == 'составить маршрут':
        await message.answer("Введите желаемую местность или город")
        await state.set_state(GetPreferences.location)

@dp.message(GetPreferences.location)
async def handle_location(message : types.Message, state : FSMContext):
    await state.update_data(location = message.text)
    await message.answer("Какой у тебя бюджет?")
    await state.set_state(GetPreferences.budget)

@dp.message(GetPreferences.budget)
async def handle_budget(message : types.Message, state : FSMContext):
    await state.update_data(budget = message.text)
    await message.answer("Какая длительность путешествия?")
    await state.set_state(GetPreferences.duration)

@dp.message(GetPreferences.duration)
async def handle_duration(message : types.Message, state : FSMContext):
    await state.update_data(duration = message.text)
    await message.answer("Какие у Вас пожелания?")
    await state.set_state(GetPreferences.interests)

@dp.message(GetPreferences.interests)
async def handle_interests(message : types.Message, state : FSMContext):
    await state.update_data(interests = message.text)
    await message.answer("Какой транспорт планируете использовать?")
    await state.set_state(GetPreferences.transport)

@dp.message(GetPreferences.transport)
async def handle_transport(message : types.Message, state : FSMContext):
    await state.update_data(transport = message.text)
    data = await state.get_data()
    await message.answer(f"{data['location']}, {data['budget']}, {data['duration']}, {data['interests']}, {data['transport']}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())