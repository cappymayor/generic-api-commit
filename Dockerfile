FROM python:3.11-slim-bookworm AS python-base

# Set API_KEY as environment variable
ENV API_KEY="d70c305e-6d11-495a-abf3-00de9615c945"

WORKDIR /data

WORKDIR /config
COPY ./config/guardian-config.yaml .

WORKDIR /scripts
COPY ./scripts/guardian-api-data.py .

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "/scripts/guardian-api-data.py", "--params", "/config/guardian-config.yaml", "--max_pages", "10"]