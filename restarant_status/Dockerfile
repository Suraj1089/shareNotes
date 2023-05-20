FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt ./app/requirements.txt


RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]