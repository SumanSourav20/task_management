FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile* ./

RUN pipenv install

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]