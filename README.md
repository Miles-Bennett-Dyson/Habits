# <p align="center">Habit Tracker — Сервис для формирования привычек</p>  
Habit Tracker — это веб-сервис для управления личными привычками с автоматизированной системой напоминаний через Telegram. Проект помогает пользователям внедрять полезные действия в повседневную жизнь, настраивать вознаграждения и отслеживать прогресс.
Адрес сервиса: http://158.160.25.183   

# <p align="center">🚀 Основные функции</p>  
- Управление привычками: Создание, редактирование и удаление личных задач.
- Публичность: Возможность просматривать привычки других пользователей (только чтение).
- Мотивация: Система вознаграждений и связанных «приятных привычек».
- Telegram-уведомления: Гибкая настройка напоминаний о необходимости выполнения действий.
- Пагинация: Список привычек разбит на страницы по 5 записей.
- API Documentation: Автоматическая генерация документации (Swagger/ReDoc).  

# <p align="center">🛠 Технологический стек</p> 
- Backend: Python, Django REST Framework (DRF)  
- Database: PostgreSQL  
- Task Queue: Celery + Redis  
- Containerization: Docker / Docker Compose  
- CI/CD: GitHub Actions  
- API Docs: Drf-yasg (Swagger)  
- Integration: Telegram Bot API

# <p align="center">📊 Модели данных</p>  

## Пользователь (User)  
Использует email как логин.  
`email, username, phone_number, avatar, tg_chat_id.`
## Привычка (Habit)  
`owner`: Создатель привычки.  
`place, time, action`: Где, когда и что нужно сделать.  
`periodicity`: Частота выполнения (от 1 до 7 дней).  
`duration`: Время на выполнение (макс. 120 сек).  
`is_pleasure`: Признак приятной привычки.  
`related_habit`: Связанная приятная привычка (для полезных привычек).  
`reward`: Вознаграждение за выполнение.  
`is_public`: Видимость для всех.  
## Привычки на сегодня (HabitsForToday)  
Служебная модель для хранения расписания на текущие сутки.  

# <p align="center">✅ Валидация данных (Бизнес-логика)</p>   
❗Исключение конфликта: Нельзя одновременно указать related_habit (связанную привычку) и reward (вознаграждение).  
⌚ Ограничение времени: Время выполнения (duration) не должно превышать 120 секунд.  
📝 Фильтр связей: В поле related_habit могут попасть только те привычки, у которых is_pleasure = True.  
📗 Приятные привычки: Сами по себе не могут иметь вознаграждения или связанных привычек.  
📊 Частота: Привычку нельзя выполнять реже, чем 1 раз в 7 дней (periodicity).  

# <p align="center">📲 Интеграция с Telegram</p>   
Рассылка напоминаний реализована через цепочку задач Celery:  
Раз в сутки (get_habits_for_today): Формируется список задач на день в модель HabitsForToday.  
Раз в час (get_tasks_in_the_next_hour): Задачи на ближайший час подгружаются в кэш.  
Ежеминутно (get_tasks_from_cache_and_send_message): Проверка кэша и отправка сообщения пользователю в Telegram.  

# <p align="center">📡 Эндпоинты API  </p>   
### Аутентификация  
POST /users/ — Регистрация.  
POST /login/ — Получение JWT-токена.  
### Привычки  
GET /habits/ — Личные привычки (пагинация по 5).  
POST /habits/ — Создание.  
PUT /habits/{id}/ — Редактирование.  
DELETE /habits/{id}/ — Удаление.  
GET /public_habits/ — Общий список публичных привычек.  
### Документация  
Swagger UI  
ReDoc  

# <p align="center">⚙️ Развертывание и CI/CD</p>   
## CI/CD (GitHub Actions)  
В репозитории настроен ci.yml. При каждом push в ветку main/develop:  
✅ Автоматически запускаются тесты.  
✅ При успешных тестах проект деплоится на удаленный сервер.  
Необходимые Secrets в GitHub:  
`DEPLOY_DIR, DOCKER_HUB_USERNAME, DOCKER_HUB_ACCESS_TOKEN, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, SECRET_KEY, SERVER_IP, SSH_KEY, SSH_USER, TELEGRAM_TOKEN, TELEGRAM_URL.`  

## Ручной деплой (Docker)
1. Подключитесь к серверу: ssh root@<server_ip>
2. Установите Docker.
3. Клонируйте репозиторий: git clone -b develop <repo_url>
4. Создайте файл .env и заполните его данными.
5. Запустите сборку:  `docker compose up -d --build`  

## Локальный запуск  
`docker compose up -d --build`   

После запуска сервис доступен по адресу: http://127.0.0.1:80
