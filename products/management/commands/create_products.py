from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Створює 4 категорії та 24 товари для магазину одягу'

    def handle(self, *args, **options):
        # 1. Створення категорій
        categories_data = [
            {"name": "Одяг", "description": "Стильний одяг для будь-якої погоди."},
            {"name": "Взуття", "description": "Зручне взуття для спорту та відпочинку."},
            {"name": "Аксесуари", "description": "Деталі, що створюють ваш образ."},
            {"name": "Сумки", "description": "Практичні та модні сумки і рюкзаки."},
        ]

        categories_dict = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={
                    "description": cat_data["description"]
                }
            )
            categories_dict[cat_data["name"]] = category

        # 2. Дані для продуктів (по 6 на категорію)
        products_data = [
            # Одяг
            {"name": "Худі Oversize", "category": "Одяг", "price": 1200.00, "description": "М'яке худі з начосом.", },
            {"name": "Джинси Straight", "category": "Одяг", "price": 1500.00, "description": "Класичні сині джинси."},
            {"name": "Футболка Свобода Слова", "category": "Одяг", "price": 450.00, "description": "Базова бавовняна футболка.", "rating": 4.5, "image": "products/clothes/white_t_shirt.jpg"},
            {"name": "Куртка-бомбер", "category": "Одяг", "price": 2800.00, "description": "Стильна демісезонна куртка."},
            {"name": "Светр вовняний", "category": "Одяг", "price": 1900.00, "description": "Теплий светр грубої в'язки.", "rating": 4.6, "image": "products/clothes/black_shirt.jpg"},
            {"name": "Шорти Cargo", "category": "Одяг", "price": 850.00, "description": "Зручні шорти з кишенями."},

            # Взуття
            {"name": "Кеди Converse", "category": "Взуття", "price": 1100.00, "description": "Легке повсякденне взуття." , "rating": 4.2, "image": "products/shoes/converse.jpg"},
            {"name": "Nike Air Max 95", "category": "Взуття", "price": 3200.00, "description": "Професійні кросівки для бігу.", "rating": 4.8, "image": "products/shoes/air_max_95.jpg"},
            {"name": "Лофери шкіряні", "category": "Взуття", "price": 2500.00, "description": "Класичне взуття для офісу.", "rating": 4.3, "image": "products/shoes/loafers.jpg"},
            {"name": "Чоботи Jumbo Geobasket", "category": "Взуття", "price": 3800.00, "description": "Високі шкіряні черевики.", "rating": 4.7, "image": "products/shoes/jumbo_geobasket.jpg"},
            {"name": "Сандалі Sport", "category": "Взуття", "price": 950.00, "description": "Зручні літні сандалі."},
            {"name": "Сліпони Minimal", "category": "Взуття", "price": 1300.00, "description": "Взуття без шнурівок.", "rating": 4.0, "image": "products/shoes/minimal_sandals.jpg"},

            # Аксесуари
            {"name": "Окуляри Aviator", "category": "Аксесуари", "price": 600.00, "description": "Сонцезахисні окуляри."},
            {"name": "Ремінь шкіряний", "category": "Аксесуари", "price": 550.00, "description": "Чорний ремінь з металевою пряжкою."},
            {"name": "Годинник Quartz", "category": "Аксесуари", "price": 2100.00, "description": "Мінімалістичний наручний годинник."},
            {"name": "Шапка Beanie", "category": "Аксесуари", "price": 350.00, "description": "Трикотажна зимова шапка."},
            {"name": "Шарф клітчастий", "category": "Аксесуари", "price": 480.00, "description": "Довгий теплий шарф."},
            {"name": "Парасолька автомат", "category": "Аксесуари", "price": 700.00, "description": "Надійна парасолька від дощу."},

            # Сумки
            {"name": "Рюкзак City", "category": "Сумки", "price": 1400.00, "description": "Міський рюкзак для ноутбука."},
            {"name": "Сумка-шопер", "category": "Сумки", "price": 300.00, "description": "Екологічна тканинна сумка."},
            {"name": "Клатч вечірній", "category": "Сумки", "price": 1800.00, "description": "Елегантна маленька сумочка."},
            {"name": "Спортивна сумка", "category": "Сумки", "price": 1100.00, "description": "Містка сумка для тренувань."},
            {"name": "Поясна сумка (Бананка)", "category": "Сумки", "price": 450.00, "description": "Зручна сумка для дрібниць."},
            {"name": "Валіза Travel Pro", "category": "Сумки", "price": 4500.00, "description": "Велика валіза на колесах."},
        ]

        # 3. Створення продуктів
        for prod_data in products_data:
            Product.objects.get_or_create(
                name=prod_data["name"],
                defaults={
                    "category": categories_dict[prod_data["category"]],
                    "description": prod_data["description"],
                    "price": prod_data["price"],
                    "rating": prod_data.get("rating", 0.0),
                    "image": prod_data.get("image", None)
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Успішно створено {len(categories_data)} категорії та {len(products_data)} товарів!'))