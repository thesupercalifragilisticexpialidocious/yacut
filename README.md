# Yacut: генерация коротких ссылок

Сервис позволяет создавать короткие ссылки и осуществлять автоматическую переадрессацию при переходе по ним. Реализована веб-страница и API.

Приложение написано на фреймворке Flask с использованием SQLAlchemy для работы с базой данных.

# Развертывание и запуск

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:thesupercalifragilisticexpialidocious/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск:

```
flask run
```

https://github.com/thesupercalifragilisticexpialidocious/
email: cmstreltsov@ya.ru