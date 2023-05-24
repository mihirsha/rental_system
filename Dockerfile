FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

CMD export PIP_DEFAULT_TIMEOUT=100

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
