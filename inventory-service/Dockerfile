
FROM python:3.9 as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .


ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]