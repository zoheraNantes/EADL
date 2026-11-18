"""Catalogue en mémoire (volontairement simple)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: Decimal
    stock: int


_PRODUCTS = {
    p.id: p
    for p in [
        Product("mug", "Mug « It works on my machine »", Decimal("12.50"), 120),
        Product("tshirt", "T-shirt « Green pipeline »", Decimal("19.90"), 40),
        Product("sticker", "Lot de stickers YAML", Decimal("2.45"), 1000),
        Product("hoodie", "Sweat « Shift left »", Decimal("44.00"), 15),
        Product("book", "Livre « Tests automatisés en 21 jours »", Decimal("29.99"), 8),
    ]
}


def list_products() -> list[Product]:
    return list(_PRODUCTS.values())


def get_product(product_id: str) -> Product:
    try:
        return _PRODUCTS[product_id]
    except KeyError:
        raise KeyError(f"Produit inconnu : {product_id}") from None
