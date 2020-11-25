import requests
from config import API_STR, DEVICE_ID, USER_ACCOUNT
import json


async def init_user():
    user = USER_ACCOUNT
    resp = requests.post(API_STR + "auth/login", json.dumps(user))
    global token_thingsboard
    token_thingsboard = resp.json()['token']


async def get_door_state(user_id):
    # req_data = {"userId": user_id}
    try:
        headers = {"X-Authorization": f"Bearer {token_thingsboard}",
                   "DeviceId": DEVICE_ID}
        serv_answer = requests.get(API_STR
                                   + "plugins/telemetry/DEVICE/"
                                   + DEVICE_ID
                                   + "/values/timeseries",
                                   params={"keys": "doorState"},
                                   headers=headers)

        if serv_answer.status_code == requests.codes.ok:
            state = int(serv_answer.json()['doorState'][0]['value'])
            state_str = "открыта" if state else "закрыта"
            message_to_user = f"Вашей дверь: **{state_str}**"
        else:
            message_to_user = "**Нет** ответа от сервера при получении статуса"
        return message_to_user
    except:
        return "**Нет** ответа от сервера при получении статуса"


async def close_door(user_id):

    # return requests.put(API_STR, req_data)
    try:
        headers = {"X-Authorization": f"Bearer {token_thingsboard}"}
        # req_data = {
        #       "method": "GE",
        #       "params": {
        #         "pin": "23",
        #         "value": 1
        #       }
        #     }
        # req_data = {"method": "getState", "params":{}}
        # json_str = json.dumps(req_data)
        # serv_answer = requests.post(API_STR
        #                             + "plugins/rpc/twoway/ce885ba0-2ea0-11eb-a6a9-95d71bacaa29",
        #                             # + DEVICE_ID,
        #                             data=json_str,
        #                             headers=headers)
        # serv_answer = requests.post(API_STR
        #                             + "plugins/rpc/twoway/ce885ba0-2ea0-11eb-a6a9-95d71bacaa29")
        # print(serv_answer.content)
        # print(serv_answer.url)
        # print(serv_answer.status_code)
        serv_answer = requests.get(API_STR
                                   + "v1/cTsUhrOX1p3o5oqmHxhW/attributes",
                                   params={'sharedKeys': "state"})
        print(serv_answer.content)
        print(serv_answer.url)
        print(serv_answer.status_code)

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
