"""Règles de calcul du panier MiniShop.

Règles métier (voir specs/pricing.feature) :
- Prix exprimés en euros TTC, arrondis au centime (ROUND_HALF_UP).
- Quantité : entier entre 1 et 99, sinon ValueError.
- Remise volume : -5 % sur une ligne dès 10 unités du même produit.
- Coupons :
    * WELCOME10 : -10 % sur le sous-total si sous-total >= 20 €
    * FIXED5    : -5 € si sous-total >= 30 €
    * FREESHIP  : livraison offerte
  Un seul coupon par panier. Coupon inconnu -> ValueError.
- Livraison : 4,90 € ; offerte si le total après remise >= 50 €.
- Panier vide : total 0, pas de frais de livraison.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from minishop.catalog import get_product

CENT = Decimal("0.01")
SHIPPING_FEE = Decimal("4.90")
FREE_SHIPPING_THRESHOLD = Decimal("50.00")
BULK_QTY = 10
BULK_RATE = Decimal("0.05")
MAX_QTY = 99
COUPONS = {"WELCOME10", "FIXED5", "FREESHIP"}


def money(value: Decimal | float | int | str) -> Decimal:
    """Arrondit un montant au centime (arrondi commercial)."""
    d = Decimal(str(value))
    # Bug injectable pour les démos de régression (MINISHOP_BUG=rounding)
    if os.getenv("MINISHOP_BUG") == "rounding":
        return d.quantize(CENT)  # ROUND_HALF_EVEN par défaut : 0.125 -> 0.12
    return d.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class Line:
    product_id: str
    qty: int
    unit_price: Decimal
    total: Decimal


@dataclass
class Quote:
    lines: list[Line] = field(default_factory=list)
    subtotal: Decimal = Decimal("0.00")
    discount: Decimal = Decimal("0.00")
    shipping: Decimal = Decimal("0.00")
    total: Decimal = Decimal("0.00")
    coupon: str | None = None

    def as_dict(self) -> dict:
        return {
            "lines": [
                {"product_id": ln.product_id, "qty": ln.qty, "unit_price": str(ln.unit_price), "total": str(ln.total)}
                for ln in self.lines
            ],
            "subtotal": str(self.subtotal),
            "discount": str(self.discount),
            "shipping": str(self.shipping),
            "total": str(self.total),
            "coupon": self.coupon,
        }


def line_total(unit_price: Decimal, qty: int) -> Decimal:
    """Total d'une ligne, remise volume incluse."""
    if not isinstance(qty, int) or isinstance(qty, bool):
        raise ValueError("La quantité doit être un entier")
    if qty < 1 or qty > MAX_QTY:
        raise ValueError(f"Quantité hors limites (1..{MAX_QTY}) : {qty}")
    gross = unit_price * qty
    if qty >= BULK_QTY:
        gross = gross * (1 - BULK_RATE)
    return money(gross)


def coupon_discount(subtotal: Decimal, coupon: str | None) -> Decimal:
    """Montant de la remise apportée par le coupon (positif)."""
    if coupon is None or coupon == "":
        return Decimal("0.00")
    code = coupon.strip().upper()
    if code not in COUPONS:
        raise ValueError(f"Coupon inconnu : {coupon}")
    if code == "WELCOME10" and subtotal >= Decimal("20"):
        return money(subtotal * Decimal("0.10"))
    if code == "FIXED5" and subtotal >= Decimal("30"):
        return Decimal("5.00")
    return Decimal("0.00")


def shipping_cost(amount_after_discount: Decimal, coupon: str | None, empty: bool) -> Decimal:
    if empty:
        return Decimal("0.00")
    if coupon and coupon.strip().upper() == "FREESHIP":
        return Decimal("0.00")
    if amount_after_discount >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")
    return SHIPPING_FEE


def quote(items: list[dict], coupon: str | None = None) -> Quote:
    """Calcule un devis pour une liste d'items {product_id, qty}."""
    q = Quote(coupon=coupon.strip().upper() if coupon else None)
    for item in items:
        product = get_product(item["product_id"])  # KeyError si inconnu
        total = line_total(product.price, item["qty"])
        q.lines.append(Line(product.id, item["qty"], product.price, total))
    q.subtotal = money(sum((ln.total for ln in q.lines), Decimal("0")))
    q.discount = coupon_discount(q.subtotal, coupon) if q.lines else Decimal("0.00")
    after = q.subtotal - q.discount
    q.shipping = shipping_cost(after, coupon, empty=not q.lines)
    q.total = money(after + q.shipping)
    return q
