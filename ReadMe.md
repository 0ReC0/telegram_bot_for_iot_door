# Telegram bot for interaction with iot door
## How to create bot
1. Open Telegram
2. Search @botfather
3. Type /newbot
4. Create bot by BotFather hints

## How to init
1. Create config.py file in the root of project
2. Init config file by template
    ```python
    TOKEN = 'token of your bot'
    API_STR = "cloud api for interaction with door"
    DEVICE_ID = "id device which you want to interact with"
    USER_ACCOUNT = {
        "username": "email",
        "password": "password"
    }
    ```
3. Run bot.py
