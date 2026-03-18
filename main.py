from pydantic import BaseModel, EmailStr, field_validator, Field, model_validator, ValidationError
from typing import Optional, Any
from datetime import datetime
import re

# ==================== МОДЕЛЬ (Задание 1 + 2) ====================
class UserRegistration(BaseModel):
    # Задание 1: Основные поля
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)
    age: int = Field(..., ge=18, le=120)
    registration_date: datetime = Field(default_factory=datetime.now)
    
    # Задание 2: Дополнительные поля
    full_name: Optional[str] = None
    phone: Optional[str] = None
    
    # ===== ВАЛИДАТОРЫ =====
    
    @field_validator('username')
    @classmethod
    def check_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Только латинские буквы, цифры и подчёркивание')
        return v
    
    @field_validator('password')
    @classmethod
    def check_password(cls, v):
        if not re.search(r'\d', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        return v
    
    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError('Пароли не совпадают')
        return self
    
    # Задание 2: Валидация full_name
    @field_validator('full_name')
    @classmethod
    def check_full_name(cls, v):
        if v is None:
            return v
        if len(v) < 2:
            raise ValueError('Имя должно содержать минимум 2 символа')
        if not v[0].isupper():
            raise ValueError('Имя должно начинаться с заглавной буквы')
        return v
    
    # Задание 2: Валидация phone
    @field_validator('phone')
    @classmethod
    def check_phone(cls, v):
        if v is None:
            return v
        pattern = r'^\+\d-\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, v):
            raise ValueError('Телефон должен быть в формате +X-XXX-XX-XX')
        return v

# ==================== ФУНКЦИЯ РЕГИСТРАЦИИ ====================
def register_user(data: dict):
    try:
        user = UserRegistration(**data)
        return {"success": True, "user": user.model_dump(exclude={'password_confirm'})}
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = error.get('loc', ['unknown'])[0]
            message = error.get('msg', 'Unknown error')
            errors.append({"field": field, "message": message})
        return {"success": False, "errors": errors}

# ==================== ЗАДАНИЕ 3*: РЕКУРСИВНАЯ МОДЕЛЬ ====================
class RecursiveNode(BaseModel):
    """Рекурсивная модель для произвольной вложенности JSON"""
    data: Any
    child: Optional['RecursiveNode'] = None

# Обновляем forward references для рекурсивной модели
RecursiveNode.model_rebuild()

def create_recursive_structure(depth: int = 3, data_value: Any = "any_data"):
    """Создаёт рекурсивную структуру заданной глубины"""
    if depth <= 0:
        return None
    return RecursiveNode(
        data=data_value,
        child=create_recursive_structure(depth - 1, data_value)
    )

def serialize_recursive_node(node: RecursiveNode) -> dict:
    """Сериализует модель в JSON-совместимый словарь"""
    if node is None:
        return None
    return node.model_dump()

# ==================== ТЕСТИРОВАНИЕ (ВСЕ ЗАДАНИЯ) ====================
if __name__ == "__main__":
    print("=" * 60)
    print("ДЗ 2: Регистрация пользователей (Задания 1, 2, 3*)")
    print("=" * 60)
    
    # ===== ТЕСТЫ ЗАДАНИЯ 1+2 =====
    print("\nТест 1: Правильные данные")
    good_data = {
        "username": "user_123",
        "email": "test@example.com",
        "password": "Password123",
        "password_confirm": "Password123",
        "age": 25,
        "full_name": "John Doe",
        "phone": "+7-999-12-34"
    }
    result = register_user(good_data)
    print(f"Успех: {result['success']}")
    if result['success']:
        user = result['user']
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Имя: {user.get('full_name')}")
        print(f"  Телефон: {user.get('phone')}")
        print(f"  Дата: {user['registration_date']}")
    
    print("\nТест 2: Ошибки валидации")
    bad_data = {
        "username": "ab",
        "email": "invalid",
        "password": "weak",
        "password_confirm": "diff",
        "age": 10,
        "full_name": "a",
        "phone": "123"
    }
    result = register_user(bad_data)
    print(f"Успех: {result['success']}")
    if not result['success']:
        print("Ошибки:")
        for err in result['errors']:
            print(f"  - {err['field']}: {err['message']}")
    
    # ===== ТЕСТ ЗАДАНИЯ 3* =====
    print("\n" + "=" * 60)
    print("ТЕСТ 3*: Рекурсивная структура")
    print("=" * 60)
    
    node = create_recursive_structure(depth=4, data_value="any_data")
    print(f"Создан узел типа: {type(node).__name__}")
    
    import json
    json_output = serialize_recursive_node(node)
    print(json.dumps(json_output, indent=2, default=str))
    
    try:
        json_str = json.dumps(json_output, default=str)
        print(f"Успешно! Длина JSON: {len(json_str)} символов")
    except TypeError as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
    print("=" * 60)
