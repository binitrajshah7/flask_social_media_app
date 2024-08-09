#Flask Dockerfile with gunicorn
FROM logitrack-base
RUN mkdir /code
WORKDIR /code
COPY app.py /code/app.py
COPY .env /code/.env
COPY lib /code/lib
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8123
CMD ["gunicorn", "--bind", "0.0.0.0:8123", "--timeout", "6000", "app:app"]