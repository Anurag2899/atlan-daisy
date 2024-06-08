# Authored by Anurag kumar

FROM python:3.9

WORKDIR /application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "data_collection.wsgi"]
