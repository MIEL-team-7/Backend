FROM python:3.12-alpine

WORKDIR /app

COPY .env.docker .env
COPY requirements.txt ../requirements.txt

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r ../requirements.txt

COPY . .

#RUN alembic upgrade head

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]