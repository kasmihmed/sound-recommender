FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./soundrecommender /code/soundrecommender

RUN python ./soundrecommender/manage.py migrate

EXPOSE 7070

CMD ["python", "./soundrecommender/manage.py", "runserver", "0.0.0.0:7070"]

