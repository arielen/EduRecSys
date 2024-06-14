# EduRecSys
__Development of a web-service recommendation system for educational services__

## Описание
Платформа для обучения 

## 📚 Навигация

- [🛠️ Установка](#️-установка)
    + [💻 Системные требования](#-системные-требования)
    + [🐍 Развертывание тестового сервера используя Python](#-запуск-тестового-сервера-с-использованием-python)
    + [🐳 Развертывание Docker Container](#-развертывание-с-docker)
- [🖼️ Визуальный интерфейс](#️-визуальный-интерфейс)


## 🛠️ Установка

### 💻 Системные требования

- **Python 3.8+**
- **Django 4.2+**
- **Виртуальное окружение** *(-опционально)*
- **Docker** *(-опционально)*
- **Docker Compose** *(-опционально)*

### 🐍 Запуск тестового сервера с использованием Python

1. **Клонируйте репозиторий:**
```sh
git clone https://github.com/arielen/EduRecSys.git
cd EduRecSys
```

2. **Создайте и активируйте виртуальное окружение:**
```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. **Установка зависимостей:**
```sh
python3 -m pip install -r backend/requirements.txt
```

4. **Примените миграции базы данных:**
```sh
python3 backend/manage.py migrate
```

5. **Создание суперпользователя:**
```sh
python3 backend/manage.py createsuperuser
```

6. **Запустите сервер разработки:**
```sh
python3 backend/manage.py runserver
```

### 🐳 Развертывание с Docker

1. **Установка Docker:** Начните с [загрузки и установки Docker](https://docs.docker.com/get-docker/) (-опционально).

2. **Перейти в директорию с проектом:**
```sh
cd backend
```

3. **Запустить Docker:**
```sh
docker build -t edu .
```

4. Откройте веб-браузер и перейдите по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).


## 🖼️ Визуальный интерфейс

![Главный интерфейс](/docs/main.png)
![Страница пользователя](/docs/profile.png)
![Редактирование оценок](/docs/mark.png)
![Прохождение тестов](/docs/softskills.png)