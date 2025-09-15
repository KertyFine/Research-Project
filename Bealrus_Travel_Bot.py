import asyncio
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "8441758015:AAEtvt2O91_t7ft1N-WU9FnLt-9IyS7YnoY"
openai.api_key = "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"

logging.basicConfig(level = logging.INFO)

bot = Bot(token = BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

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


@dp.message(lambda message: message.text and message.text.lower() == "составить маршрут")
async def restart_route(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите желаемую местность и город")
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

"""async def ask_neural_network(preferences: dict) -> str:
    # Формируем запрос текстом
    prompt = (
        f"Составь маршрут по Беларуси на основе следующих данных:\n"
        f"Локация: {preferences['location']}\n"
        f"Бюджет: {preferences['budget']}\n"
        f"Длительность: {preferences['duration']}\n"
        f"Интересы: {preferences['interests']}\n"
        f"Транспорт: {preferences['transport']}\n\n"
        "Напиши подробный маршрут."
    )
    # Вызов OpenAI Completion
    response = await asyncio.to_thread(lambda: openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    ))
    # Парсим результат
    return response['choices'][0]['message']['content']

@dp.message(GetPreferences.transport)
async def handle_transport(message: types.Message, state: FSMContext):
    await state.update_data(transport=message.text)
    data = await state.get_data()
    result_text = await ask_neural_network(data)
    await message.answer(result_text)"""