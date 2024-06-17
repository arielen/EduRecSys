# EduRecSys
__Development of a web-service recommendation system for educational services__

## 🧭 Навигация
- [🧭 Навигация](#-навигация)
- [📌 Описание](#-описание)
- [🖼️ Визуальный интерфейс](#️-визуальный-интерфейс)
    + [👥 Пользовательский интерфейс](#-пользовательский-интерфейс)
    + [👨‍💼 Интерфейс администратора](#-интерфейс-администратора)
    + [🔗 Другие изображения](https://github.com/arielen/EduRecSys/tree/master/docs/images.md)
- [🛠️ Установка](#️-установка)
    + [💻 Системные требования](#-системные-требования)
    + [🐍 Развертывание тестового сервера используя Python](#-запуск-тестового-сервера-с-использованием-python)
    + [🐳 Развертывание Docker Container](#-развертывание-с-docker)
- [📝 Планируемые обновления](#-планируемые-обновления)

## 📌 Описание
Веб-сервис, предназначенный для персонализированной рекомендации образовательных мероприятий, таких как олимпиады и конкурсы, на основе индивидуальных оценок и тестирования мягких навыков (*soft skills*).

**Основные функции и возможности:**

- **Оценка мягких навыков:**
    + Проведение специализированных тестов для выявления уровня развития различных soft skills, таких как коммуникабельность, креативность, критическое мышление, работа в команде и другие.
    + Анализ результатов тестирования для создания профиля пользователя.

- **Профиль пользователя:**
    + Возможность заполнения пользователем анкет и оценок по различным критериям, включая академические достижения, интересы, цели и предпочтения.
    + Сохранение истории пройденных тестов и заполненных анкет для точного отслеживания прогресса и обновления рекомендаций.

- **Персонализированные рекомендации:**
    + Генерация списка рекомендуемых олимпиад и конкурсов на основе анализа профиля пользователя и его soft skills.
    + Учёт интересов пользователя и целей развития при подборе рекомендаций, что позволяет предлагать наиболее подходящие мероприятия.

- **Интерактивный интерфейс:**
    + Удобный и интуитивно понятный интерфейс, обеспечивающий лёгкий доступ к результатам тестов и рекомендациям.
    + Визуализация прогресса пользователя и динамики развития его soft skills.

- **Обратная связь и поддержка:**
    + Возможность получения обратной связи от экспертов по результатам тестов и рекомендациям.
    + Доступ к материалам для самоподготовки и повышения уровня soft skills.

**Преимущества:**

- **Индивидуальный подход:** Каждому пользователю предоставляются рекомендации, соответствующие его уникальным навыкам и интересам.
- **Повышение шансов на успех:** Рекомендации помогают пользователям выбирать наиболее подходящие олимпиады и конкурсы, что повышает их шансы на победу и признание.
- **Удобство и доступность:** Онлайн-доступ к сервису позволяет пользователям получать рекомендации в любое время и из любого места.

Ваш надёжный помощник в мире образовательных мероприятий, направленных на раскрытие потенциала и развитие навыков!

## 🖼️ Визуальный интерфейс

### 👥 Пользовательский интерфейс
https://github.com/arielen/EduRecSys/assets/69113994/e8cbf88b-2063-4ca7-ad36-7f72bee3e06c

### 👨‍💼 Интерфейс администратора
![Интерфейс администратора](/docs/interface_admin.gif)

[🔗 Дополнительные изображения](https://github.com/arielen/EduRecSys/tree/master/docs/images.md)

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


## 📝 Планируемые обновления

- [ ] 🚧 **Интеграция Redis** для повышения производительности и скорости обработки данных.
- [ ] **OAuth-аутентификация с сервисами VKGroup и Yandex** для упрощения входа пользователей через их учетные записи в этих системах.
- [ ] 🚧 **Полное REST API** для более удобного и эффективного взаимодействия между клиентом и сервером.
- [ ] **Редизайн пользовательского интерфейса** с целью улучшения визуального восприятия и удобства использования.
- [ ] **Увеличение безопасности** за счет внедрения дополнительных мер защиты данных и шифрования.
- [ ] **Создание и обновление документации** для отражения всех новых функций и улучшений, что облегчит работу с системой разработчикам и пользователям.
- [ ] **Интеграция аналитических инструментов** для отслеживания и анализа пользовательского поведения и метрик производительности.
- [ ] 🚧 **Внедрение системы уведомлений** для своевременного информирования пользователей о важных событиях и обновлениях.


<p align="right"><a href="#top">🔼 Вернуться выше</a></p>
