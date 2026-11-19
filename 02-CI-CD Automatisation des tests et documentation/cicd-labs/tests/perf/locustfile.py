"""Test de charge Locust (Atelier 10).

Interactif :  locust -f tests/perf/locustfile.py --host http://localhost:8000   -> http://localhost:8089
CI (headless, avec seuils) :
  locust -f tests/perf/locustfile.py --host http://localhost:8000 --headless -u 50 -r 10 -t 1m \
         --csv reports/perf --html reports/perf.html
Les seuils (SLO) ci-dessous font échouer le run (code retour 1) s'ils ne sont pas tenus.
"""

import random

from locust import HttpUser, between, events, task

SLO_P95_MS = 300
SLO_ERROR_RATE = 0.01
PRODUCTS = ["mug", "tshirt", "sticker", "hoodie", "book"]


class Client(HttpUser):
    wait_time = between(0.5, 2)

    @task(5)
    def catalogue(self):
        self.client.get("/products")

    @task(3)
    def fiche_produit(self):
        self.client.get(f"/products/{random.choice(PRODUCTS)}", name="/products/{id}")

    @task(3)
    def devis(self):
        items = [{"product_id": random.choice(PRODUCTS), "qty": random.randint(1, 12)}]
        self.client.post("/cart/quote", json={"items": items, "coupon": random.choice([None, "WELCOME10"])})

    @task(1)
    def commande(self):
        self.client.post("/orders", json={"items": [{"product_id": "mug", "qty": 1}]})


@events.quitting.add_listener
def check_slo(environment, **_kwargs):
    stats = environment.stats.total
    p95 = stats.get_response_time_percentile(0.95)
    err = stats.fail_ratio
    print(f"\n== SLO == p95={p95:.0f} ms (max {SLO_P95_MS}) | erreurs={err:.2%} (max {SLO_ERROR_RATE:.0%})")
    if p95 > SLO_P95_MS or err > SLO_ERROR_RATE:
        print("SLO NON RESPECTÉ -> échec du job")
        environment.process_exit_code = 1
