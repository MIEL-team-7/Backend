FROM python:3.12-alpine

WORKDIR /app

COPY .env.docker .env
COPY requirements.txt ../requirements.txt

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r ../requirements.txt

COPY . .

CMD alembic upgrade head

EXPOSE 8000
