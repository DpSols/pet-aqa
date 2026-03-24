FROM python:3.14-slim

# psycopg[binary] requires libpq; playwright chromium requires system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# playwright install must come AFTER pip install playwright
RUN playwright install --with-deps chromium

COPY docker .
ENTRYPOINT ["pytest"]
CMD ["tests/api", "tests/web", "-m", "api or web", "--alluredir=allure-results"]
