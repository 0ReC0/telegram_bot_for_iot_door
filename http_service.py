import requests
from config import API_STR, DEVICE_ID, USER_ACCOUNT, ACCESS_TOKEN
import json


async def init_user():
    user = USER_ACCOUNT
    resp = requests.post(API_STR + "auth/login", json.dumps(user))
    global token_thingsboard
    token_thingsboard = resp.json()['token']


async def get_door_state(user_id):
    try:
        headers = {"X-Authorization": f"Bearer {token_thingsboard}"}
        serv_answer = requests.get(API_STR
                                   + "plugins/telemetry/DEVICE/"
                                   + DEVICE_ID
                                   + "/values/timeseries",
                                   headers=headers)

        if serv_answer.status_code == requests.codes.ok:
            state = int(serv_answer.json()['doorOpen'][0]['value'])
            state_str = "открыта" if state else "закрыта"
            message_to_user = f"Вашей дверь: **{state_str}**"
        else:
            message_to_user = "**Нет** ответа от сервера при получении статуса"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"


async def close_door(user_id):
    try:
        data = {'doorOpen': 0}
        data = json.dumps(data)
        serv_answer = requests.post(API_STR
                                    + f"v1/{ACCESS_TOKEN}/telemetry",
                                    data=data)

        if serv_answer.status_code == requests.codes.ok:
            door_state = await get_door_state(user_id)
            message_to_user = "Состояние двери обновлено \n" + door_state
        else:
            message_to_user = "**Нет** ответа от сервера при закрытии двери"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"


async def open_door(user_id):
    try:
        data = {'doorOpen': 1}
        data = json.dumps(data)
        serv_answer = requests.post(API_STR
                                    + f"v1/{ACCESS_TOKEN}/telemetry",
                                    data=data)
        if serv_answer.status_code == requests.codes.ok:
            door_state = await get_door_state(user_id)
            message_to_user = "Состояние двери обновлено \n" + door_state
        else:
            message_to_user = "**Нет** ответа от сервера при закрытии двери"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"
