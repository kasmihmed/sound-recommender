FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./soundrecommender /code/soundrecommender


EXPOSE 8080

CMD ["python", "./soundrecommender/manage.py", "runserver", "8080"]

