FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /site

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /site

CMD ["python", "main.py"]