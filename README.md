# <p align="center">Habit Tracker — Сервис для формирования привычек  </p>

## <p align="center">Описание проекта</p>  

Сервис для управления личными привычками с возможностью настройки напоминаний через Telegram. Позволяет создавать полезные и приятные привычки, настраивать вознаграждения и получать уведомления о необходимости выполнения действий.  

## <p align="center">Основные функции</p>  

- Регистрация и авторизация пользователей.
- Создание, редактирование и удаление личных привычек.
- Просмотр публичных привычек (только чтение).
- Пагинация списка привычек (5 записей на страницу).
- Интеграция с Telegram для рассылки напоминаний.
- Валидация данных согласно бизнес‑логике.
- Настройка CORS для взаимодействия с фронтендом.
- Автоматическая документация API.
  
---

## <p align="center">Требования</p>
<table align="center" >
  <tr>
     <th> Python 3.10+ </th>
     <th> Django REST Framework </th>
     <th> PostgreSQL </th>
  </tr>
  <tr>
     <th>Poetry</th>
     <th>Django 4.2+</th>
    <th>Celery </th>
   </tr>
  <tr>
    <th>Telegram Bot API</th>
    <th>CI/CD</th>
    <th>Redis</th>
  </tr>
</table>
  
---
## <p align="center">CI/CD</p>
В репозитории имеется ci.yml для GitHub Actions который запускет тесты проекта автоматически при каждом push в репозиторий. Так же автоматически деплоит проект на удаленный сервер после успешного прохождения тестов.
Для успешного деплоя, вам нужно указать в Actions secrets значения для:
- DEPLOY_DIR
- DOCKER_HUB_ACCESS_TOKEN
- DOCKER_HUB_USERNAME
- POSTGRES_DB
- POSTGRES_HOST
- POSTGRES_PASSWORD
- POSTGRES_PORT
- POSTGRES_USER
- SECRET_KEY
- SERVER_IP
- SSH_KEY
- SSH_USER
- TELEGRAM_TOKEN
- TELEGRAM_URL

Для деплоя вручную, используйте следующие шаги:
1. Зайдите на ваш сервер через SSH: ssh root@ip-вашего-сервера
2. Установите Docker: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
3. Сгенерируйте SSH-ключ на сервере и добавьте его в GitHub, либо используйте токен (PAT). Склонируйте репозиторий: git clone -b develop git@github.com:ваш-логин/имя-репозитория.git
4. Файлы .env не передаются через Git. Вам нужно создать его на сервере вручную: nano .env
5. Соберите и запустите образ командой: docker compose up -d --build
6. Проверить запущенные контейнеры можно командой docker ps. Посмотреть все контейнеры командой: docker ps -a. Либо перейдите на ваш сервер в браузере по ip адресу.

## <p align="center">Модели данных </p> 
### <p align="center">Модель «Привычка» (Habit)</p> 
<p align="center">Модель используется для хранения всех привычек.  </p> 
<table align="center" >
  <tr>
     <th> Поле </th>
    <th> Тип </th>
    <th> Описание </th>
  </tr>
    <tr>
     <th> owner </th>
    <th> ForeignKey </th>
    <th> Пользователь‑создатель привычки </th>
  </tr>
    <tr>
     <th> place </th>
    <th> String </th>
    <th> Место выполнения привычки </th>
  </tr>
   <tr>
     <th> time </th>
    <th> Time </th>
    <th> Время выполнения привычки </th>
  </tr>
  <tr>
     <th> action </th>
    <th> String </th>
    <th> Действие, составляющее привычку </th>
  </tr>
   <tr>
     <th> next_due_date </th>
    <th> Date </th>
    <th> Следующая дата выполнения </th>
  </tr>
  <tr>
     <th> is_pleasure </th>
    <th> Boolean </th>
    <th> Признак приятной привычки </th>
  </tr>
   <tr>
     <th> related_habit </th>
    <th> ForeignKey (null)</th>
    <th> Связанная приятная привычка </th>
  </tr>
     <tr>
     <th> periodicity </th>
    <th> Integer (default=1)</th>
    <th> Периодичность выполнения (в днях, min: 1, max: 7) </th>
  </tr>
     <tr>
     <th> reward </th>
    <th> String (null)</th>
    <th> Вознаграждение за выполнение </th>
  </tr>
     <tr>
     <th> duration </th>
    <th> Time </th>
    <th> Длительность выполнения (max: 120 s)</th>
  </tr>
     <tr>
     <th> is_public </th>
    <th> Boolean (default=False)</th>
    <th> Признак публичности привычки </th>
  </tr>
</table>
  
---

### <p align="center">Модель «Привчки на сегодняшний день» (HabitsForToday)
<p align="center">Модель используется для хранения привычек которые будут выполнятся на сегодняшний день.  </p> 
<table align="center" >
  <tr>
     <th> Поле </th>
    <th> Тип </th>
    <th> Описание </th>
  </tr>
    <tr>
     <th> habit </th>
    <th> ForeignKey </th>
    <th> Привычка из модели Habits </th>
  </tr>
    <tr>
     <th> time </th>
    <th> Time </th>
    <th> Назначенное время выполнения привычки </th>
  </tr>
  </table>
  
---

### <p align="center">Модель «Пользователь» (User)</p> 
<p align="center">Модель является стандартной, наследуется от класса AbstractUser. Авторизация происходит по email.  </p> 
<p align="center">Добавлены дополнительные поля:</p> 
<table align="center" >
  <tr>
     <th> Поле </th>
    <th> Тип </th>
    <th> Описание </th>
  </tr>
  <tr>
    <th> username </th>
    <th> String </th>
    <th> Никнейм </th>
  </tr> 
  <tr>
     <th> email </th>
    <th> String </th>
    <th> Электронная почта </th>
  </tr>
    <tr>
     <th> phone_number </th>
    <th> String </th>
    <th> Номер телефона </th>
  </tr>

  <tr>
    <th> avatar </th>
    <th> Image </th>
    <th> Аватар </th>
  </tr>
    <tr>
     <th> tg_chat_id </th>
    <th> Integer </th>
    <th> ID чата в телеграмм </th>
  </tr>
  </table>  
  
  ------------------------------

  ## <p align="center">Валидация данных </p> 
  - Исключение конфликта: нельзя одновременно указать related_habit и reward.
  - Время выполнения: duration ≤ 120 секунд.
  - Связанные привычки: в related_habit могут быть только привычки с is_pleasure = True.
  - Приятные привычки: не могут иметь reward или related_habit.
  - Периодичность: 1 ≤ periodicity ≤ 7 дней.
    
---

 ## <p align="center">Эндпоинты API </p> 

 ### <p align="center">Регистрация и аутентификация</p>   
`POST /users/` — регистрация пользователя.

`POST /login/` — получение JWT‑токена.

 ### <p align="center">Управление привычками</p>   
 
`GET /habits/` — список личных привычек с пагинацией (5 на страницу).

`GET /public_habits/` — список публичных привычек с пагинацией (5 на страницу).

`POST /habits/` — создание новой привычки.

`PUT /habits/{id}/` — редактирование привычки.

`DELETE /habits/{id}/` — удаление привычки.  

---

 ## <p align="center">Документация API</p> 
 Документация доступна по адресу:  
http://your-domain/swagger/ для Swagger UI  
http://your-domain/redoc/ для Redoc.    

---

 ## <p align="center">Интеграция с Telegram</p> 

- Пользователь связывает свой аккаунт с Telegram‑ботом.
- Сервис планирует отложенные задачи (Celery) для напоминаний.
- Бот отправляет уведомления в указанное время.
Расписание отложенных задач записано в `settings.py`. Каждый день задачей `get_habits_for_today()` берется из модели те прввычки которые должны будут выполнятся сегодня.
 Далее они добавляются в модель HabitsForToday. Каждый час задача `get_tasks_in_the_next_hour()` получает задачи на текущий час и добавляет их в кэш. Следющая зачада `get_tasks_from_cache_and_send_message()` ежеминутно проверяет кэш и отправляет уведомленя пользователям.
    
---

 
 
