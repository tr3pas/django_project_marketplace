# Dice & Dragons

Фентезійний інтернет-магазин настільних ігор на Django. Стилізований під магічну крамницю — кожна категорія виглядає як гільдія, кожна гра — як артефакт з іншого світу.

## Стек

- Python 3.12 / Django 6.0.2
- SQLite (розробка)
- Redis (опційно, для кешування)
- django-ratelimit (захист від брутфорсу)
- Django Debug Toolbar

## Додатки

| Додаток | Призначення |
|---------|-------------|
| `products` | Каталог: моделі `Category` та `Product`, пошук, кешування категорій |
| `account` | Реєстрація / вхід, профіль, адреса доставки |
| `cart` | Кошик (БД для авторизованих, сесія для анонімних) |
| `order` | Оформлення замовлення, історія замовлень |

## Встановлення та запуск

```bash
# Клонувати репозиторій
git clone <url>
cd django_project_marketplace

# Створити та активувати віртуальне середовище
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# Встановити залежності
pip install django pillow python-dotenv django-redis django-ratelimit debug-toolbar django-allauth requests pyjwt cryptography

# Створити .env файл
cp .env.example .env  # або створити вручну

# Застосувати міграції
python manage.py migrate

# Наповнити БД тестовими даними
python manage.py create_products

# Запустити сервер
python manage.py runserver
```

Відкрити у браузері: http://127.0.0.1:8000

## Змінні середовища (`.env`)

```env
SECRET_KEY = your-secret-key
DEBUG = 'True'
ALLOWED_HOSTS = 'localhost,127.0.0.1'

CLIENT_ID_GOOGLE = your_id
CLIENT_SECRET_GOOGLE = your-secret-key
REDIS_URL=redis://localhost:6379/0   # опційно
```

Якщо `REDIS_URL` не задано — використовується `LocMemCache`.

## URL-маршрути

| URL | Опис |
|-----|------|
| `/` | Головна сторінка |
| `/categories/` | Список категорій |
| `/categories/<slug>/` | Ігри певної категорії |
| `/products/` | Каталог усіх ігор |
| `/products/<slug>/` | Картка товару |
| `/cart/` | Кошик |
| `/order/checkout/` | Оформлення замовлення |
| `/order/history/` | Історія замовлень |
| `/account/register/` | Реєстрація |
| `/account/login/` | Вхід |
| `/account/profile/` | Профіль користувача |
| `/accounts` | Вхід через Google
| `/admin/` | Адмін-панель |

## Тести

```bash
python manage.py test              # усі тести
python manage.py test products
python manage.py test cart
python manage.py test account
python manage.py test order
```

## Ключові особливості

- **Кошик**: двохрежимний — для авторизованих користувачів зберігається в БД (`Cart`/`CartItem`), для анонімних — у сесії.
- **Кешування**: список категорій,продуктів кешується на 30 хвилин; скидається автоматично через сигнали при зміні `Category` або `Product`.
- **Захист**: `@ratelimit` на ендпоінтах входу та реєстрації (100 запитів/хв з IP).
- **Замовлення**: `OrderItem` зберігає знімок назви та ціни товару на момент покупки.
- **Slug**: автогенерується з `name` при першому збереженні моделей `Category` і `Product`.