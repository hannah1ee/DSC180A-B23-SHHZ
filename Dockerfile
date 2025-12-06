FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install https://github.com/anishathalye/semlib/archive/refs/heads/master.zip

CMD ["python", "main.py"]
