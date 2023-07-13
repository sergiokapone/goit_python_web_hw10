# Установка зависимостей
FROM python:3.10

# Установка pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Копирование Pipfile и Pipfile.lock
WORKDIR /app
COPY Pipfile* /app/

# Установка зависимостей с помощью pipenv
RUN pipenv install

# Копирование приложения
COPY . /app

# Копирование .env файла
COPY .env /app

# Запуск приложения
CMD ["pipenv", "run", "python", "hw10/manage.py", "runserver"]
