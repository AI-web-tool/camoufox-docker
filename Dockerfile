FROM python:3.12-slim

# System dependencies required by Camoufox/Firefox
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgtk-3-0 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxshmfence1 \
    libdbus-glib-1-2 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir camoufox[geoip]

# Fetch browser binaries and addons
RUN python -m camoufox fetch

COPY start.py /app/start.py

EXPOSE 9222

CMD ["python", "/app/start.py"]
