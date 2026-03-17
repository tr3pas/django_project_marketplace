from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = "Створює 4 категорії та 24 товари для магазину одягу"

    def handle(self, *args, **options):
        # 1. Створення категорій
        categories_data = [
            {"name": "Одяг", "description": "Стильний одяг для будь-якої погоди."},
            {
                "name": "Взуття",
                "description": "Зручне взуття для спорту та відпочинку.",
            },
            {"name": "Аксесуари", "description": "Деталі, що створюють ваш образ."},
            {"name": "Сумки", "description": "Практичні та модні сумки і рюкзаки."},
        ]

        categories_dict = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"], defaults={"description": cat_data["description"]}
            )
            categories_dict[cat_data["name"]] = category

        # 2. Дані для продуктів (по 6 на категорію)
        products_data = [
            # Одяг
            {
                "name": "Худі Oversize",
                "category": "Одяг",
                "price": 1200.00,
                "description": "М'яке худі з начосом.",
                "color": "Чорний",
                "size": "L",
                "rating": 4.5,
                "image": "products/clothes/black_shirt_oversize.webp",
            },
            {
                "name": "Джинси Straight",
                "category": "Одяг",
                "price": 1500.00,
                "description": "Класичні сині джинси.",
                "color": "Синій",
                "size": "35",
                "rating": 4,
                "image": "products/clothes/jeans_acne_studios.jpg",
            },
            {
                "name": "Футболка Свобода Слова",
                "category": "Одяг",
                "price": 450.00,
                "description": "Базова бавовняна футболка.",
                "color": "Білий",
                "size": "M",
                "rating": 4.5,
                "image": "products/clothes/white_t_shirt.jpg",
            },
            {
                "name": "Куртка-бомбер",
                "category": "Одяг",
                "price": 2800.00,
                "description": "Стильна демісезонна куртка.",
                "color": "Чорний",
                "size": "XL",
                "rating": 4.2,
                "image": "products/clothes/black_jacket.webp",
            },
            {
                "name": "Светр вовняний",
                "category": "Одяг",
                "price": 1900.00,
                "description": "Теплий светр грубої в'язки.",
                "color": "Чорний",
                "size": "L",
                "rating": 4.6,
                "image": "products/clothes/black_shirt.jpg",
            },
            {
                "name": "Шорти Cargo",
                "category": "Одяг",
                "price": 850.00,
                "description": "Зручні шорти з кишенями.",
                "color": "Чорний",
                "size": "35",
                "rating": 4.0,
                "image": "products/clothes/black_shorts.webp",
            },
            # Взуття
            {
                "name": "Кеди Converse",
                "category": "Взуття",
                "price": 1100.00,
                "description": "Легке повсякденне взуття.",
                "color": "Чорний",
                "size": "42",
                "rating": 4.2,
                "image": "products/shoes/converse.jpg",
            },
            {
                "name": "Nike Air Max 95",
                "category": "Взуття",
                "price": 3200.00,
                "description": "Професійні кросівки для бігу.",
                "color": "Білий",
                "size": "45",
                "rating": 4.8,
                "image": "products/shoes/air_max_95.jpg",
            },
            {
                "name": "Лофери шкіряні",
                "category": "Взуття",
                "price": 2500.00,
                "description": "Класичне взуття для офісу.",
                "color": "Чорний",
                "size": "43",
                "rating": 4.3,
                "image": "products/shoes/loafers.jpg",
            },
            {
                "name": "Чоботи Jumbo Geobasket",
                "category": "Взуття",
                "price": 3800.00,
                "description": "Високі шкіряні черевики.",
                "color": "Чорний",
                "size": "44",
                "rating": 4.7,
                "image": "products/shoes/jumbo_geobasket.jpg",
            },
            {
                "name": "Чорні Crocs",
                "category": "Взуття",
                "price": 950.00,
                "description": "Зручні літні сандалі.",
                "color": "Чорний",
                "size": "42",
                "rating": 4.1,
                "image": "products/shoes/crocs.webp",
            },
            {
                "name": "Nike Dunk White",
                "category": "Взуття",
                "price": 1300.00,
                "description": "Взуття без шнурівок.",
                "color": "Білий",
                "size": "45",
                "rating": 4.0,
                "image": "products/shoes/dunk.jpg",
            },
            # Аксесуари
            {
                "name": "Окуляри Chrome Hearts",
                "category": "Аксесуари",
                "price": 600.00,
                "description": "Сонцезахисні окуляри.",
                "rating": 4.0,
                "image": "products/accessories/chrome_hearts_glasses.jpg",
            },
            {
                "name": "Ремінь шкіряний Chrome Hearts",
                "category": "Аксесуари",
                "price": 550.00,
                "description": "Чорний ремінь з металевою пряжкою.",
                "rating": 4.2,
                "image": "products/accessories/belt.png",
            },
            {
                "name": "Годинник Casio",
                "category": "Аксесуари",
                "price": 2100.00,
                "description": "Мінімалістичний наручний годинник.",
                "rating": 4.5,
                "image": "products/accessories/clock_casio.jpg",
            },
            {
                "name": "Шапка чорна",
                "category": "Аксесуари",
                "price": 350.00,
                "description": "Трикотажна зимова шапка.",
                "rating": 4.1,
                "image": "products/accessories/black_hat.webp",
            },
            {
                "name": "Шарф клітчастий Burberry",
                "category": "Аксесуари",
                "price": 480.00,
                "description": "Довгий теплий шарф.",
                "rating": 4.3,
                "image": "products/accessories/scarf.webp",
            },
            {
                "name": "Парасолька автомат",
                "category": "Аксесуари",
                "price": 700.00,
                "description": "Надійна парасолька від дощу.",
                "rating": 4.2,
                "image": "products/accessories/umbrella.jpg",
            },
            # Сумки
            {
                "name": "Рюкзак City The North Face",
                "category": "Сумки",
                "price": 1400.00,
                "description": "Міський рюкзак для ноутбука.",
                "color": "Чорний",
                "rating": 4.4,
                "image": "products/bags/backpack.webp",
            },
            {
                "name": "Сумка-шопер ERD",
                "category": "Сумки",
                "price": 300.00,
                "description": "Екологічна тканинна сумка.",
                "rating": 4.0,
                "color": "Чорний",
                "image": "products/bags/shoper_erd.webp",
            },
            {
                "name": "Клатч чорний",
                "category": "Сумки",
                "price": 1800.00,
                "description": "Елегантна маленька сумочка.",
                "rating": 4.5,
                "color": "Чорний",
                "image": "products/bags/clutch.jpg",
            },
            {
                "name": "Спортивна сумка Patagonia",
                "category": "Сумки",
                "price": 1100.00,
                "description": "Містка сумка для тренувань.",
                "color": "Зелений",
                "rating": 4.2,
                "image": "products/bags/sport_bag_patagonia.webp",
            },
            {
                "name": "Поясна сумка Levis",
                "category": "Сумки",
                "price": 450.00,
                "description": "Зручна сумка для дрібниць.",
                "color": "Синій",
                "rating": 4.1,
                "image": "products/bags/bag_levis.jpg",
            },
            {
                "name": "Валіза Marvel",
                "category": "Сумки",
                "price": 4500.00,
                "description": "Велика валіза на колесах.",
                "color": "Червоний",
                "rating": 4.6,
                "image": "products/bags/travel_luggage.jpg",
            },
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
                    "color": prod_data.get("color", ""),
                    "size": prod_data.get("size", ""),
                    "image": prod_data.get("image", None),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Успішно створено {len(categories_data)} категорії та {len(products_data)} товарів!"
            )
        )
