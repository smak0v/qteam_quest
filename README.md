# QTeam Quest Project

## Установка и запуск сервиса

Для локальустановки и запуска сервиса нужно выполнить дальнейшие шаги.

### Подготовка базы данных

1. Установить ```PostgreSQL```.

2. Открыть консоль или командную строку, войти в ```PostgreSQL``` под пользователем ```postgres```.

3. Создать базу данных ```qteam_quest```:

    ```
    CREATE DATABASE qteam_quest;
    ```

4. Создать пользователя ```qteam_quest_user``` с паролем ```qteam_quest_user_password```:

    ```
    CREATE USER qteam_quest_user WITH PASSWORD 'qteam_quest_user_password';
    ```

5. Дать созданому пользователю все права и разрешения на взаимодействие с базой данных ```qteam_quest```:

    ```
    GRANT ALL PRIVILEGES ON DATABASE qteam_quest TO qteam_quest_user;
    ```

### Подготовка окружения

1. Установить ```Python 3.7```.

2. Установить модуль для создания виртуального окружения выполнив следующую команду в терминале или командной стркое:

    ```
    $ pip install virtualenv
    ```

3. Перейти в директорию с проектом.

4. Создать виртуальное окружение:

    ```
    $ virtualenv venv
    ```

5. Активировать виртуальное окружение:

    - для пользователей Unix OS / Mac OS:

        ```
        $ source venv/bin/activate
        ```

    - для пользователей Windows OS:

        ```
        $ cd venv
        $ cd Scripts
        $ activate
        $ cd ..
        $ cd ..
        ```

6. Установить зависимости для проекта:

    ```
    (venv)$ pip install -r requirements.txt
    ```

7. Установить ```Redis``` с помощью следующей команды в терминале:

    ```
    $ sudo apt install redis
    ```

8. Проверить корректность установки ```Redis``` с помощью следующей команды в терминале:

    ```
   $ redis-cli ping
    ```

   В ответ в терминале должно появится сообщение ```PONG```.

### Подготовка и запуск сервиса

1. Выполнить миграции в базу данных:

    ```
    (venv)$ python manage.py migrate
    ```

2. Запустить сервис:

    ```
    (venv)$ python manage.py runserver
    ```

3. Открыть второе окно терминала, активировать виртуальное окружение проекта в нем и выполнить следующую команду:

    ```
   (venv)$ celery -A qteam_quest worker -l info
   ```

4. Открыть третье окно терминала, активировать виртуальное окружение проекта в нем и выполнить следующую команду:

    ```
   (venv)$ celery -A qteam_quest beat -l info
    ``` 

5. Для заполнения базы данных тестовым набором данных выполнить команду в терминале:

    ```
    (venv)$ python manage.py fill_db
    ```

6. Для удаления всей информации с базы данных (кроме суперпользователей) выполнить команду в терминале:

    ```
    (venv)$ python manage.py clear_db
    ```

7. Перейти в браузере по адресу ```http://127.0.0.1:8000```.
