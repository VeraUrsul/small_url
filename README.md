# small_url

### Описание
Small URL - веб сервис, помогающий укоротить URL или сам придумает для Вас короткий вариант.

### Технологии

- Python 3.9.13
- Flask 2.0.2
- Werkzeug 2.0.2
- SQLAlchemy 1.4.29

### Как пользоваться сайтом

 - В первое окно необходимо указать ссылку, для которой Вы хотите создать короткий вариант. 
 - Во втором окне можно указать короткий вариант идентификатора (до 16 символов). Это окно не обязательное и его можно оставить пустым. В таком случае короткая ссылка сгенерируется автоматически.

### Как запустиль проект

# 1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:VeraUrsul/small_url.git
cd small_url
```

# 2. Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

# 3. Установить зависимости из файла requirements.txt:

```
# Обновить пакет pip
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
# 4. Создать файл .env и заполнить

```
touch .env
nano .env
FLASK_APP=small_url
# определить среду запуска приложения — «продакшена» или разработки
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=funfunfun
```

# 5. Применить миграции

```
flask db upgrade
```

# 6. Запуск интерактивной оболочки Flask Shell

```
flask shell
# Создайте таблицы
>>> from small_url import db
>>> db.create_all()
```
# 7. Запуск приложения Flask

```
flask run
```

## Документация API  при работающем сервере [OpenAPI](http://127.0.0.1:5000/docs)

### Автор [Урсул Вера](https://github.com/VeraUrsul)

