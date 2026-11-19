FROM python:3.12-slim
WORKDIR /app
# Correctifs de sécurité Debian publiés depuis la construction de l'image de base (cf. Trivy, Atelier 11)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY minishop ./minishop
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "minishop.api:app", "--host", "0.0.0.0", "--port", "8000"]
