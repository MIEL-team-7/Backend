# Miel

Бекенд часть проекта для риелторской сети [Miel](https://miel.ru/)


## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/MIEL-team-7/Backend
cd Backend
```

### 2. Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate # Для Linux/MacOS
venv/Scripts/activate    # Для Windows
pip install -r requirements.txt
```

### 3. Запуск сервера

```bash
python app/main.py
```

Сервер доступен по адресу http://127.0.0.1:8000

### 4. Документация

- [Swagger UI](http://127.0.0.1:8000/docs)

- [Redoc](http://127.0.0.1:8000/redoc)

- [OpenAPI](http://127.0.0.1:8000/openapi.json)


## Разработка

Разработка проходит в ветке `dev`
```bash
git switch dev # Для того, чтобы перейти в ветку dev
git branch --set-upstream-to origin/dev # Для того, чтобы указать ветку dev как ветку по умолчанию
git pull origin dev # Для того, чтобы обновить ветку dev
git push origin dev # Для того, чтобы отправить ветку dev
```

Работа с ветками
```bash
git branch -b <название_ветки> # Для того, чтобы создать ветку <название_ветки>
git switch <название_ветки> # Для того, чтобы перейти в ветку <название_ветки>
git push origin <название_ветки> # Для того, чтобы запушить ветку <название_ветки>