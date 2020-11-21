from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_getState = InlineKeyboardButton('Получить состояние двери', callback_data='getState')
button_closeDoor = InlineKeyboardButton('Закрыть дверь', callback_data='closeDoor')
button_openDoor = InlineKeyboardButton('Открыть дверь', callback_data='openDoor')
button_pollingDoor = InlineKeyboardButton('Запустить получение оповещения о состоянии двери каждую минуту',
                                          callback_data='pollingDoor')

inline_keyboard = InlineKeyboardMarkup()
inline_keyboard\
    .add(button_getState)\
    .add(button_closeDoor)\
    .add(button_openDoor)\
    .add(button_pollingDoor)

polling_close_kb = ReplyKeyboardMarkup(resize_keyboard=True)
polling_close_kb.add(KeyboardButton('/stopPolling'))
