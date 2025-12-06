FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/BioCypher/semlib.git

CMD ["python", "main.py"]
