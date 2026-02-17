from dataclasses import dataclass
from fastapi import FastAPI, HTTPException


app = FastAPI()

products = [
    {
        "id": 1,
        "name": "Wireless Noise-Cancelling Headphones",
        "description": "Premium over-ear headphones with active noise cancellation and 30-hour battery life.",
        "price": 149.99,
        "stock": 230,
    },
    {
        "id": 2,
        "name": "Bamboo Mechanical Keyboard",
        "description": "Eco-friendly mechanical keyboard with cherry MX switches and a natural bamboo frame.",
        "price": 89.95,
        "stock": 75,
    },
    {
        "id": 3,
        "name": "Smart LED Desk Lamp",
        "description": "Adjustable color-temperature desk lamp with app control and USB charging port.",
        "price": 42.50,
        "stock": 410,
    },
    {
        "id": 4,
        "name": "Titanium Insulated Water Bottle",
        "description": "Double-walled 750ml bottle that keeps drinks cold for 24 hours or hot for 12.",
        "price": 34.99,
        "stock": 520,
    },
    {
        "id": 5,
        "name": "Portable Espresso Maker",
        "description": "Hand-powered espresso machine for brewing barista-quality coffee on the go.",
        "price": 64.00,
        "stock": 185,
    },
    {
        "id": 6,
        "name": "Ergonomic Standing Desk Mat",
        "description": "Anti-fatigue gel mat with textured massage zones for comfortable standing work.",
        "price": 55.75,
        "stock": 310,
    },
    {
        "id": 7,
        "name": "Solar-Powered Backup Charger",
        "description": "20,000mAh portable charger with dual solar panels and fast-charge USB-C output.",
        "price": 79.99,
        "stock": 142,
    },
    {
        "id": 8,
        "name": "Canvas Laptop Backpack",
        "description": "Water-resistant waxed canvas backpack with a padded 15-inch laptop compartment.",
        "price": 112.00,
        "stock": 67,
    },
    {
        "id": 9,
        "name": "Mini Air Quality Monitor",
        "description": "Compact sensor that tracks CO2, humidity, temperature, and VOC levels in real time.",
        "price": 98.50,
        "stock": 203,
    },
    {
        "id": 10,
        "name": "Magnetic Cable Organizer Set",
        "description": "Pack of 5 silicone magnetic clips to keep charging cables tidy on any desk surface.",
        "price": 14.99,
        "stock": 870,
    },
]


@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    stock: int


class ProductsService:
    def __init__(self):
        self.all_product: list = []
        for product in products:
            new_product = Product(
                product["id"],
                product["name"],
                product["description"],
                product["price"],
                product["stock"],
            )
            self.all_product.append(new_product)

    def get_all_products(self) -> list[Product]:
        return self.all_product

    def get_product_by_id(self, product_id: int) -> Product | None:
        for product in self.all_product:
            if product.id == product_id:
                return product
        return None


product_manager = ProductsService()


@app.get("/products")
async def all_products():
    return product_manager.get_all_products()


@app.get("/products/{product_id}")
async def specific_product(product_id: int):
    specific_product1 = product_manager.get_product_by_id(product_id)
    if specific_product1 is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return specific_product1
