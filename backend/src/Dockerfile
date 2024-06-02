FROM python:3.10.12

WORKDIR /readings/src

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --reload"]"]