FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN  python manage.py collectstatic --noinput
RUN  python manage.py migrate
RUN  python manage.py create_products

EXPOSE 8000

CMD ["gunicorn", "django_project_marketplace.wsgi:application", "--bind", "0.0.0.0:8000"]