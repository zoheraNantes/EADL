"""Client LLM minimal, compatible avec toute API « OpenAI chat/completions ».

Choix du fournisseur par variables d'environnement :

  LLM_PROVIDER=anthropic -> API Claude d'Anthropic (ANTHROPIC_API_KEY), via le SDK
                           officiel `anthropic` — fournisseur recommandé du cours
  LLM_PROVIDER=ollama   -> Ollama (http://localhost:11434), sans clé ni compte :
                           modèle léger qwen2.5-coder:1.5b (~1 Go), utilisable
                           sur le poste comme sur un runner de CI
  LLM_PROVIDER=mistral  -> API Mistral (MISTRAL_API_KEY)
  LLM_PROVIDER=openai   -> API OpenAI (OPENAI_API_KEY)
  LLM_PROVIDER=offline  -> pas d'appel réseau (les outils basculent sur une
                           implémentation déterministe « simulée »)

Surcharges possibles : LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, LLM_TIMEOUT (secondes),
LLM_EFFORT (anthropic : low | medium | high).

(GitHub Models, utilisé dans les versions précédentes de ce cours, a été arrêté
par GitHub le 30 juillet 2026.)

Usage :
    from ai_tools.llm import chat, is_offline
    print(chat("Tu es un testeur.", "Liste 3 cas limites pour une division."))
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request

PROVIDERS = {
    "anthropic": {
        "base_url": "https://api.anthropic.com",
        "model": "claude-haiku-5-5",  # économique ; plus capable : LLM_MODEL=claude-sonnet-5-5
        "key_env": "ANTHROPIC_API_KEY",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5-coder:1.5b",  # machine puissante : LLM_MODEL=qwen2.5-coder:7b
        "key_env": None,
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "model": "mistral-small-latest",
        "key_env": "MISTRAL_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
        "key_env": "OPENAI_API_KEY",
    },
}


class LLMError(RuntimeError):
    pass


def provider() -> str:
    return os.getenv("LLM_PROVIDER", "offline").lower()


def is_offline() -> bool:
    return provider() == "offline"


def _config() -> tuple[str, str, str | None]:
    name = provider()
    if name not in PROVIDERS:
        raise LLMError(f"LLM_PROVIDER inconnu : {name} (choix : {', '.join(PROVIDERS)}, offline)")
    cfg = PROVIDERS[name]
    base = os.getenv("LLM_BASE_URL", cfg["base_url"]).rstrip("/")
    model = os.getenv("LLM_MODEL", cfg["model"])
    key = os.getenv("LLM_API_KEY") or (os.getenv(cfg["key_env"]) if cfg["key_env"] else None)
    if cfg["key_env"] and not key:
        raise LLMError(f"Variable {cfg['key_env']} (ou LLM_API_KEY) manquante pour {name}")
    return base, model, key


def _chat_anthropic(system: str, user: str, model: str, key: str | None) -> str:
    """Appel de l'API Messages d'Anthropic avec le SDK officiel (pas de `temperature` sur les
    modèles récents : la profondeur de raisonnement se règle avec `effort`)."""
    try:
        import anthropic
    except ImportError as exc:
        raise LLMError("Paquet `anthropic` absent : pip install anthropic") from exc
    options = {"api_key": key, "timeout": float(os.getenv("LLM_TIMEOUT", "600"))}
    if os.getenv("LLM_BASE_URL"):
        options["base_url"] = os.environ["LLM_BASE_URL"]
    client = anthropic.Anthropic(**options)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=16000,  # inclut le raisonnement du modèle : ne pas descendre trop bas
            system=system,
            output_config={"effort": os.getenv("LLM_EFFORT", "medium")},
            messages=[{"role": "user", "content": user}],
        )
    except anthropic.AuthenticationError as exc:
        raise LLMError(f"Clé Anthropic refusée (HTTP 401) : {exc.message}") from exc
    except anthropic.RateLimitError as exc:
        raise LLMError(f"Quota ou débit Anthropic dépassé (HTTP 429) : {exc.message}") from exc
    except anthropic.APIStatusError as exc:
        raise LLMError(f"HTTP {exc.status_code} : {exc.message}") from exc
    except anthropic.APIConnectionError as exc:
        raise LLMError(f"Connexion impossible à l'API Anthropic : {exc}") from exc
    if response.stop_reason == "refusal":
        raise LLMError("Le modèle a refusé de répondre à cette demande (stop_reason=refusal)")
    text = "".join(block.text for block in response.content if block.type == "text")
    if not text.strip():
        raise LLMError(f"Réponse vide de l'API Anthropic (modèle {model}, arrêt : {response.stop_reason})")
    return text


def chat(system: str, user: str, temperature: float = 0.2, max_tokens: int = 2500) -> str:
    """Envoie un prompt et renvoie le texte de la réponse."""
    if is_offline():
        raise LLMError("Mode offline : aucun appel LLM possible")
    base, model, key = _config()
    if provider() == "anthropic":
        return _chat_anthropic(system, user, model, key)
    body = json.dumps(
        {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }
    ).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(f"{base}/chat/completions", data=body, headers=headers)
    try:
        # Délai large par défaut : un petit modèle local sur CPU met plusieurs minutes
        with urllib.request.urlopen(req, timeout=float(os.getenv("LLM_TIMEOUT", "600"))) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        raise LLMError(f"HTTP {exc.code} : {exc.read().decode(errors='replace')[:500]}") from exc
    except urllib.error.URLError as exc:
        raise LLMError(f"Connexion impossible à {base} : {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:  # délai dépassé pendant la lecture, connexion coupée...
        raise LLMError(f"Pas de réponse exploitable de {base} : {exc}") from exc
    except ValueError as exc:  # réponse 200 qui n'est pas du JSON (proxy d'entreprise, portail captif...)
        raise LLMError(f"Réponse non JSON de {base} (proxy ?) : {exc}") from exc
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"Réponse inattendue de {base} : {str(data)[:300]}") from exc
    if not isinstance(content, str) or not content.strip():
        raise LLMError(f"Réponse vide de {base} (modèle {model})")
    return content


_FENCE = re.compile(r"```[ \t]*([\w+-]*)[ \t]*\r?\n(.*?)```", re.S)


def extract_code(text: str, lang: str = "python") -> str:
    """Récupère le premier bloc ```python ...``` d'une réponse (ou le texte brut).

    À défaut de bloc étiqueté `lang`, prend le premier bloc de code quel que soit
    son étiquette (```py, ``` sans langage...) ; l'étiquette n'est jamais recopiée.
    """
    blocks = _FENCE.findall(text)
    for tag, code in blocks:
        if tag.lower() == lang:
            return code.strip() + "\n"
    if blocks:
        return blocks[0][1].strip() + "\n"
    # Bloc ouvert mais jamais refermé (réponse tronquée par max_tokens)
    if m := re.search(r"```[ \t]*[\w+-]*[ \t]*\r?\n(.*)", text, re.S):
        return m.group(1).strip() + "\n"
    return text.strip() + "\n"


if __name__ == "__main__":
    print(f"Fournisseur : {provider()}")
    if is_offline():
        print("Mode offline : aucun appel LLM, les outils utilisent leur moteur déterministe.")
        print("Pour un vrai LLM : export LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=<clé>   (ou mistral, ollama)")
        raise SystemExit(0)
    try:
        print(chat("Tu réponds en une phrase.", "Qu'est-ce qu'un test de régression ?"))
    except LLMError as exc:
        raise SystemExit(f"[x] LLM indisponible : {exc}") from None
