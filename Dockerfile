FROM python:3.12-slim

RUN apt-get update && apt-get install -y wget
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/local/bin/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

WORKDIR /app

COPY .env.docker .env
COPY requirements.txt ../requirements.txt

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r ../requirements.txt

COPY . .

CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh db:5432 -- alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

EXPOSE 8000
