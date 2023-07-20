FROM python
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]