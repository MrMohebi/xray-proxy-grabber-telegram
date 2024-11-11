FROM python:3.9.0-slim
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]