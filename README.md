# HORO_AIOGRAM_BOT

##### Стек: Python, Aiogram, Beautifulsoup, httpx, Apscheduler, asyncpg
***

### Что умеет HORO_AIOGRAM_BOT
Телеграм бот на aiogram, который присылает гороскопы.
Доступные команды: 
```
/start - cтартовая команда
/help - для получения всех доступных команд
/update - для получения нового гороскопа
/change_zodiac - для изменения знака зодиака
/clear_history - для удаления истории сообщений
/real_horoscope - для получения реального гороскопа на сегодня
```

В наличии есть 6 разных гороскопов, которые не зависят от знака зодиака.
За день можно получить 6 гороскопов. 

Доступно получение реального гороскопа с сервиса horoscopes.rambler.ru.
С помощью beautifulsoup достается текст гороскопа для конкретного знака зодиака.

Также можно удалить историю сообщений за последние 48 часов (ограничение telegram)

***
### Запуск проекта

Для запуска проекта необходимо: 

Копировать репозиторий:
```
git clone git@github.com:pashpiter/horo-aiogram-bot.git
```
Перейти в папку с кодом бота:
```
cd horo-aiogram-bot
```
Установить зависимости:
```
poetry install
```
Создать и заполнить файл .env по примеру (.env_example) или:
```
BOT_TOKEN = 'token' (Токен бота, можно получить в BotFather)
DB_USER = postgres (Имя пользовтеля БД)
DB_HOST = localhost (Хост БД)
DB_PASSWORD = postgres (Пароль пользователя БД)
DB_NAME = postgres (Название БД)
DB_PORT = 5432 (Порт БД)
```
Запустить бот:
```
python main.py
``` 
или 
```
make up
```