FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Don't run as root
RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python", "bot.py"]
