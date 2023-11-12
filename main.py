import SQL_DB
import asyncio
import logging
import sys
import Buttons as bt
import Texts as txt
import Encrypt as en
import Decrypt as de

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

BOT_TOKEN = "Введите токен"

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

sql_db = SQL_DB.Data_Base()

class States(StatesGroup):  # Класс состояний
    shifr = State()  # Состояние шифровки
    deshifr = State()  # Состояние дешифровки


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.reply(f'Добро пожаловать, {hbold(message.from_user.full_name)} !\n'
                        f'\n'
                        f'{txt.greeting_message}', reply_markup=bt.keyboard)


async def shifr_message(message: Message, state: FSMContext):
    text_input = await en.message_input(message.text.split('#')[0], int(message.text.split('#')[1]))
    await message.answer(text_input)
    await sql_db.add_data_shifr(message.from_user.id, message.text.split('#')[0], int(message.text.split('#')[1]),text_input)
    await state.clear()


async def deshifr_message(message: Message, state: FSMContext):
    text_output = await de.message_output(message.text.split('#')[0], int(message.text.split('#')[1]))
    await message.answer(text_output)
    await sql_db.add_data_deshifr(message.from_user.id, message.text.split('#')[0], int(message.text.split('#')[1]),text_output)
    await state.clear()


@dp.message(F.text.lower() == '🔐 зашифровать сообщение')
async def encrypt(message: types.Message, state: FSMContext):
    await state.set_state(States.shifr)
    await message.answer(f'{txt.shifr_text}')


@dp.message(F.text.lower() == '🔓 расшифровать сообщение')
async def decrypt(message: types.Message, state: FSMContext):
    await state.set_state(States.deshifr)
    await message.answer(f'{txt.deshifr_text}')


@dp.message(F.text.lower() == '📄 описание')
async def description(message: types.Message):
    await message.answer(f'{txt.description}')


dp.message.register(shifr_message, States.shifr)
dp.message.register(deshifr_message, States.deshifr)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
