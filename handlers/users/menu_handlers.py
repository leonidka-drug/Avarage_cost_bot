from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.default import menu
from data.conf import GH_data
from data.config import DATA_BASE_FILE
from utils.db_api.sqlite import Database
from utils.google_sheets.calculations import calculate_cost

db = Database(DATA_BASE_FILE)


@dp.message_handler(Command('start'))
async def show_menu(message: Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer("Выбери действие", reply_markup=menu)


@dp.message_handler(text="Посмотреть средний чек номера")
async def show_average_cost(message: Message):
    params = await calculate_cost(GH_data['sofia'])
    full_info = 'За {} дней средний чек: {:.2f},\nНедостача: {:.2f},'.format(
        params["days_gone"],
        params["sold_average"],
        params["shortage"],
    )
    full_info += '\nСредний чек за номер на следующие дни: {:.2f}'.format(
        params["next_days_cost"])
    full_info += '\nМинимальна сумма прихода на следующие дни: {:.2f}'.format(
        params["next_days_cost"] * params["number_of_rooms"])

    await message.answer(text=full_info)
