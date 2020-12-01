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
    TELEGRAM_BOT_TOKEN = 'token of your bot'
    API_STR = "cloud api for interaction with door"
    DEVICE_ID = "id device which you want to interact with"
    ACCESS_TOKEN = "access token of your device"
    USER_ACCOUNT = {
        "username": "email",
        "password": "password"
    }
    ```
3. Run bot.py
## How to use bot
1. Send ```/start``` to bot in telegram, u will see all available commands
    
    Commands: 
    
        * ```/start``` - connect with bot
        * ```/help``` - open list of all available commands
        * ```/getKb``` - open keyboard of bot
        * ```/stopPolling``` - this is needed to stop polling which started in keyboard of bot
2. Send ```/getKb``` to open keyboard
    * 1 option (RU (Получить состояние двери)) - get door state
    * 2 option (RU (Закрыть дверь)) - close door
    * 3 option (RU (Открыть дверь)) - open door
    * 4 option (RU (Запустить получение оповещения о состоянии двери каждую минуту)) - start long polling cloud to get door state every 60 sec

