"""Récepteur de webhooks Alertmanager minimal (Atelier 12) : affiche les alertes reçues.

Alertmanager (monitoring/alertmanager.yml) envoie ses notifications sur
http://host.docker.internal:5001/alert ; ce script les affiche dans le terminal.

Usage :
    python scripts/alert_receiver.py            # écoute sur 0.0.0.0:5001 (Ctrl+C pour arrêter)
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802 (nom imposé par http.server)
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            payload = json.loads(body or b"{}")
        except ValueError:
            payload = {}
        for alert in payload.get("alerts", []):
            labels, notes = alert.get("labels", {}), alert.get("annotations", {})
            print(
                f"[{alert.get('status', '?').upper():8}] {labels.get('alertname', '?')} "
                f"({labels.get('severity', '-')}) — {notes.get('summary', '')}",
                flush=True,
            )
        self.send_response(200)
        self.end_headers()

    def log_message(self, *_args):  # pas de journal HTTP : on n'affiche que les alertes
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    print(f"En attente des alertes sur http://0.0.0.0:{port}/alert ...")
    try:
        # 0.0.0.0 : le conteneur Alertmanager doit pouvoir joindre le poste (Docker sous Linux)
        HTTPServer(("0.0.0.0", port), Handler).serve_forever()  # noqa: S104
    except KeyboardInterrupt:
        pass
