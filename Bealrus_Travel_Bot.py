import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from openai import OpenAI

BOT_TOKEN = "8441758015:AAEtvt2O91_t7ft1N-WU9FnLt-9IyS7YnoY"

logging.basicConfig(level = logging.INFO)

bot = Bot(token = BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

kb_builder = ReplyKeyboardBuilder()
kb_builder.add(KeyboardButton(text = "Составить маршрут"), KeyboardButton(text = "Узнать о месте"), KeyboardButton(text = "Ещё варианты"))
kb_builder.adjust(3)
reply_kb = kb_builder.as_markup(resize_keyboard = True)


class GetPreferences(StatesGroup):
    location = State()
    budget = State()
    duration = State()
    interests = State()
    transport = State()

class InfoPLace(StatesGroup):
    place = State()

async def ask_ai(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-chat-v3.1:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


@dp.message(Command("start"))
async def cmd_start(message : types.Message, state : FSMContext):
    await message.answer("Привет! Я бот для генерации маршрутов по Беларуси.", reply_markup = reply_kb)

@dp.message(lambda message : message.text and message.text.lower() == "узнать о месте")
async def info_about_get_place(message : types.Message, state: FSMContext):
    await message.answer("Введите название места, о котором хотите узнать информацию")
    await state.set_state(InfoPLace.place)

@dp.message(InfoPLace.place)
async def info_about_place(message : types.Message, state : FSMContext):
    place = message.text
    result = await ask_ai(f"Расскажи про это место: {place}. Ответ дай конкретным сообщением 100-300 символов."
                          f"Укажи в сообщении название места и чем оно является, например, столицей")
    await message.answer(f'{result}')

@dp.message(lambda message: message.text and message.text.lower() == "составить маршрут")
async def start_getting_preferences(message: types.Message, state: FSMContext):
    await state.clear()
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
    result = await ask_ai(
        f"Сгенерируй маршрут по данным. Местность: {data['location']}, бюджет: {data['budget']}, длительность: {data['duration']}, пожелания: {data['interests']}, транспорт: {data['transport']}."
        f"Маршрут должен проходить только по тем местам, которые расположены в этой местности."
        f"Если маршрут занимает несколько дней, укажи конкретное место, где можно переночевать(отель, хостел, гостиница и т.д.(также ты указываешь очень заниженные цены, исправь это: указывай цены в 1.5-2 раза больше)), указывай реально существующие места."
        f"Ответ дай сообщением 100-300 символов."
        f"Если какой-то параметр не соответствует описанию, попробуй догадаться, что пользователь имел в виду и укажи ему на это")
    await message.answer(f'{result}')

@dp.message(lambda message : message.text and (message.text.lower() == "еще варианты" or message.text.lower() == "ещё варианты"))
async def another_route(message : types.Message, state : FSMContext):
    data = await state.get_data()
    result = await ask_ai(
        f"Сгенерируй маршрут по данным. Местность: {data['location']}, бюджет: {data['budget']}, длительность: {data['duration']}, пожелания: {data['interests']}, транспорт: {data['transport']}."
        f"Маршрут должен проходить только по тем местам, которые расположены в этой местности, используя транспорт, который указан."
        f"Если маршрут занимает несколько дней, укажи конкретное место, где можно переночевать(отель, хостел, гостиница и т.д.(также ты указываешь очень заниженные цены, исправь это: указывай цены в 1.5-2 раза больше)), указывай реально существующие места."
        f"Ответ дай сообщением 100-300 символов."
        f"Если какой-то параметр не соответствует описанию, попробуй догадаться, что пользователь имел в виду и укажи ему на это")
    await message.answer(f'{result}')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())