import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import text

from config import TOKEN
import keyboards as kb
import http_service

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

polling_task = None

help_message = text(
    "Доступные команды:\n",
    "/start - приветствие",
    "/help - помощь с командами",
    "/getKb - открыть клавиатуру",
    # "/cancel - закрыть клавиатуру",
    "/stopPolling - остановка оповещения каждую минуту",
    sep="\n"
)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\n Это магическая дверь =)")

    await http_service.init_user()

    await message.reply(help_message)


@dp.message_handler(commands=['getKb'])
async def process_start_command(message: types.Message):
    await message.reply("Открываю клавиатуру", reply_markup=kb.inline_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'getState')
async def process_callback_get_state(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(callback_query.from_user.id, "Окей, сейчас посмотрю, что там с ней")

    message_to_user = await http_service.get_door_state(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, message_to_user, parse_mode=ParseMode.MARKDOWN_V2)


@dp.callback_query_handler(lambda c: c.data == 'closeDoor')
async def process_callback_get_state(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(callback_query.from_user.id, "Такс, закрываю...")

    message_to_user = await http_service.close_door(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, message_to_user, parse_mode=ParseMode.MARKDOWN_V2)


@dp.callback_query_handler(lambda c: c.data == 'openDoor')
async def process_callback_get_state(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(callback_query.from_user.id, "Понял, сейчас открою =)")

    message_to_user = await http_service.open_door(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, message_to_user, parse_mode=ParseMode.MARKDOWN_V2)


async def custom_polling(wait_for, user_id):
    while True:
        await asyncio.sleep(wait_for)

        message_to_user = await http_service.get_door_state(user_id)
        await bot.send_message(user_id, message_to_user, parse_mode=ParseMode.MARKDOWN_V2)


@dp.callback_query_handler(lambda c: c.data == 'pollingDoor')
async def process_callback_get_state(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(callback_query.from_user.id, "Окей, сейчас буду оповещать")

    time_to_hold_s = 60
    await bot.send_message(callback_query.from_user.id, "Для завершения нажмите "
                                                        "на кнопку на встроенной клавиатуре",
                           reply_markup=kb.polling_close_kb)

    global polling_task
    polling_task = asyncio.create_task(custom_polling(time_to_hold_s, callback_query.from_user.id))
    await polling_task


@dp.message_handler(commands=['stopPolling'])
async def process_help_command(message: types.Message):
    if polling_task:
        polling_task.cancel()
        await message.reply('Останавливаю оповещение и закрываю клавиатуру =)', reply_markup=kb.ReplyKeyboardRemove())
    else:
        await message.reply('Не вижу оповещений', reply_markup=kb.ReplyKeyboardRemove())


# @dp.message_handler(commands=['cancel'])
# async def process_help_command(message: types.Message):
#     await message.reply('Закрываю встроенную клавиатуру =)', reply_markup=kb.ReplyKeyboardRemove())\


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
