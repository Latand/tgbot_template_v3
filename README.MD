Цей темплейт використовується для розробки Telegram ботів з використанням бібліотеки [`aiogram v3.0+`](https://github.com/aiogram/aiogram/tree/dev-3.x).

## SQLAlchemy + Alembic
В коді є приклади таблички User з використанням SQLAlchemy 2.0, та скрипти для алембіку (ініціалізація алембік, створення та застосування міграцій).

Але, якщо ви з цими інструментами ніколи не працювали, то зверніться до документації і дізнайтесь про ці інструменти. 
Також, в мене є англомовний [курс по цим інструментам на Udemy](https://www.udemy.com/course/sqlalchemy-alembic-bootcamp/?referralCode=E9099C5B5109EB747126).

![img.png](https://img-c.udemycdn.com/course/240x135/5320614_a8af_2.jpg)

### Для того, щоб почати використовувати:
1. Скопіюйте `.env.dist` в `.env` і заповніть необхідні дані.
2. Створіть нові хендлери.
3. **Docker:**
   1. Можете одразу запускати проєкт із Docker, а якщо в вас його немає, то [завантажте, та встановіть](https://docs.docker.com/get-docker/).
   2. Запустіть проєкт з команди `docker-compose up`
4. **Без Docker:**
   1. Створіть [venv](https://docs.python.org/3/library/venv.html)
   2. Встановить залежності із requirements.txt: `pip install -r requirements.txt --pre`
   3. Запустіть проєкт з команди `python3 bot.py`


### Як робити та реєструвати хендлери:
Створюєте модуль `you_name.py` у папці `handlers`.

Створюєте роутер у `you_name.py`.
```python
from aiogram import Router
user_router = Router()
```
Можна робити декілька роутерів в одному модулі, та на кожний з них навішувати хендлери.
Можна реєструвати хендлери декораторами:
```python
@user_router.message(commands=["start"])
async def user_start(message):
    await message.reply("Вітаю, звичайний користувач!")
```

Заходимо у файл `handlers/__init__.py` і додаємо всі роутери в нього:
```python
from .admin import admin_router
from .echo import echo_router
from .user import user_router

...


routers_list = [
    admin_router,
    user_router,
    echo_router,  # echo_router must be last
]

```
### Як додати хендлери до нашого бота:
Переходимо до файлу  `bot.py` та розпаковуємо наші хендлери:
```python
from tgbot.handlers import routers_list

...

async def main():
   
    ...

   dp.include_routers(*routers_list)

    ...


```

### Як запустити Базу Данних та провести свою першу міграцію:
1. Перейдіть до `.env` файлу та заповніть дані для бази даних, якщо ви не зробили цього раніше.

2. Перейдіть до файлу `docker-compose.yml` та розкоментуйте секції: `api`, `pg_database` і `volumes`, щоб розпочати роботу.

3. Перейдіть до `config.py` та виконайте `TODO` в функції `construct_sqlalchemy_url`. Також знайдіть розділ функції `load_config` і розкоментуйте рядок, що відповідає ініціалізації конфігурації бази даних `db=DbConfig.from_env(env)`, щоб активувати підключення до бази даних.

4. Тепер можемо перезапустити Docker з новими контейнерами, використовуючи команду:

    `docker-compose up --build.`

5. Все готово! Тепер можемо провести міграцію!
Відкрийте термінал та введіть наступну команду:

    `docker-compose exec api alembic upgrade head`

### Туторіали з aiogram v3
Відосів поки що немає, але @Groosha вже почав робити [свій підручник](https://mastergroosha.github.io/aiogram-3-guide).
