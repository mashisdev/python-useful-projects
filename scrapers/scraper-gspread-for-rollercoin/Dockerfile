FROM python:3.12.10-alpine3.21

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python3", "./main.py" ]