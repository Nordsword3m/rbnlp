FROM python:3.12
RUN apt-get update
RUN apt-get install -y awscli
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src /app
CMD ["fastapi", "run", "main.py", "--port", "80"]