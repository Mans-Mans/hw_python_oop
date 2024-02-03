**Готовый функционал**
* Создать, прочитать, удалить, изменить документ.
* Создать, прочитать, удалить, изменить папку.
* Создать, удалить, изменить ресурс документа.
* Документы могут храниться в папках.
* Папки могут храниться в папках.
* Пользователь может дать доступ на прочтени к отдельному документу или файлу.
* Для проосмотра всех документов и папок пользователя не нужна регистрация.
* Для детального просмотра отдельного документа или папки нужен доступ.

### Стек технолигий
* Python 3.11
* Django 4.2.3
* djangorestframework 3.14.0
* Redis 4.6.0
* Gunicorn 20.1.0
* Celery 5.3.1
* Docker

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@gitlab.it-psg.com:ib-elp-it-psg/documents_management_module.git
```

```
cd documents_module
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Создайте суперюзера:

```
python manage.py createsuperuser
```

Придумайте пароль и логин. 
Запустите сервер:

```

python manage.py runserver

```

По ссылке http://127.0.0.1:8000/api/redoc/ будет доступа API документация.
