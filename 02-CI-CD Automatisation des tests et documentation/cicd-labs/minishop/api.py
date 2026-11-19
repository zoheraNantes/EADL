"""API HTTP MiniShop (FastAPI).

Lancer :  uvicorn minishop.api:app --reload
Docs   :  http://localhost:8000/docs   (OpenAPI : /openapi.json)
"""

from __future__ import annotations

import json
import logging
import os
import random
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field

from minishop import __version__
from minishop.catalog import get_product, list_products
from minishop.pricing import quote

STATIC = Path(__file__).parent / "static"
LOG_FILE = os.getenv("MINISHOP_LOG_FILE")  # ex. logs/app.jsonl

logger = logging.getLogger("minishop")
logger.setLevel(logging.INFO)
if LOG_FILE:
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    logger.addHandler(logging.FileHandler(LOG_FILE))

REQUESTS = Counter("minishop_http_requests_total", "Requêtes HTTP", ["method", "path", "status"])
LATENCY = Histogram("minishop_http_request_duration_seconds", "Latence HTTP", ["path"])
ORDERS = Counter("minishop_orders_total", "Commandes créées")

app = FastAPI(title="MiniShop", version=__version__, description="Application fil rouge de la formation CI/CD & IA")
app.mount("/static", StaticFiles(directory=STATIC), name="static")

_ORDERS: dict[str, dict] = {}


class Item(BaseModel):
    product_id: str = Field(examples=["mug"])
    qty: int = Field(ge=1, le=99, examples=[2])


class Cart(BaseModel):
    items: list[Item] = Field(default_factory=list)
    coupon: str | None = Field(default=None, examples=["WELCOME10"])


@app.middleware("http")
async def observe(request: Request, call_next):
    start = time.perf_counter()
    if os.getenv("MINISHOP_BUG") == "slow" and request.url.path.startswith("/cart"):
        time.sleep(random.uniform(0.3, 0.8))
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    path = request.scope.get("route").path if request.scope.get("route") else request.url.path
    REQUESTS.labels(request.method, path, response.status_code).inc()
    LATENCY.labels(path).observe(elapsed)
    logger.info(
        json.dumps(
            {
                "ts": time.time(),
                "method": request.method,
                "path": path,
                "status": response.status_code,
                "latency_ms": round(elapsed * 1000, 2),
            }
        )
    )
    return response


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__}


@app.get("/metrics", include_in_schema=False)
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/products")
def products():
    return [{"id": p.id, "name": p.name, "price": str(p.price), "stock": p.stock} for p in list_products()]


@app.get("/products/{product_id}")
def product(product_id: str):
    try:
        p = get_product(product_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None
    return {"id": p.id, "name": p.name, "price": str(p.price), "stock": p.stock}


def _quote(cart: Cart):
    try:
        return quote([i.model_dump() for i in cart.items], cart.coupon)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc).strip("'")) from None
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None


@app.post("/cart/quote")
def cart_quote(cart: Cart):
    return _quote(cart).as_dict()


@app.post("/orders", status_code=201)
def create_order(cart: Cart):
    if not cart.items:
        raise HTTPException(status_code=422, detail="Panier vide")
    q = _quote(cart)
    order_id = uuid.uuid4().hex[:12]
    _ORDERS[order_id] = {"id": order_id, **q.as_dict()}
    ORDERS.inc()
    return _ORDERS[order_id]


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in _ORDERS:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return _ORDERS[order_id]
