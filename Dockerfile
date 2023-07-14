FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt --timeout=2000

COPY . .

COPY ./entrypoint.sh /

EXPOSE 8000

ENTRYPOINT [ "sh", "/entrypoint.sh" ]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
