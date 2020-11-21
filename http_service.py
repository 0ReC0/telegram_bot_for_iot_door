import requests
from config import API_STR


async def get_door_state(user_id):
    req_data = {"userId": user_id}
    # return requests.get(API_STR, req_data)
    try:
        serv_answer = requests.get(API_STR)
        if serv_answer.status_code == requests.codes.ok:
            state = serv_answer.text
            state_str = "открыта" if state else "закрыта"
            message_to_user = f"Вашей дверь: **{state_str}**"
        else:
            message_to_user = "**Нет** ответа от сервера при получении статуса"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"


async def close_door(user_id):
    req_data = {"userId": user_id, "doorState": False}
    # return requests.put(API_STR, req_data)
    try:
        serv_answer = requests.put(API_STR)
        if serv_answer.status_code == requests.codes.ok:
            door_state = await get_door_state(user_id)
            message_to_user = "Состояние двери обновлено \n" + door_state
        else:
            message_to_user = "**Нет** ответа от сервера при закрытии двери"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"


async def open_door(user_id):
    req_data = {"userId": user_id, "doorState": True}
    # return requests.put(API_STR, req_data)
    try:
        serv_answer = requests.put(API_STR)
        if serv_answer.status_code == requests.codes.ok:
            door_state = await get_door_state(user_id)
            message_to_user = "Состояние двери обновлено \n" + door_state
        else:
            message_to_user = "**Нет** ответа от сервера при закрытии двери"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"
