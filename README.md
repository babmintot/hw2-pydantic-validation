# Валидация данных с Pydantic (ДЗ 2)

**Дисциплина:** Разработка прототипов программных решений  
**Тема:** FastAPI и Pydantic  
**Преподаватель:** Владимир Хомутов  
**Вебинар:** Тема 2 — Сериализация данных

## 📋 Задание 1: Регистрация пользователей

Модель `UserRegistration` с валидацией:

| Поле | Тип | Требования |
|---|---|---|
| username | str | 3-20 символов, латиница+цифры+_ |
| email | EmailStr | Валидный email-адрес |
| password | str | Мин. 8 символов, цифры, заглавные и строчные буквы |
| password_confirm | str | Должен совпадать с password |
| age | int | 18-120 включительно |
| registration_date | datetime | Автоматически (default_factory) |
| full_name | Optional[str] | Заглавная буква, мин. 2 символа |
| phone | Optional[str] | Формат +X-XXX-XX-XX |

## 📋 Задание 2: Дополнение

Добавлены поля `full_name` и `phone` с кастомными валидаторами.

## ⭐ Задание 3: Рекурсивная модель

Создана модель `RecursiveNode` для произвольной вложенности JSON.

## 🚀 Запуск

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
.\venv\Scripts\Activate.ps1

# Установить зависимости
pip install -r requirements.txt

# Запустить тесты
python main.py