FROM python:3.10-slim-buster

WORKDIR /app

#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
RUN pip3 install requests
RUN pip3 install lxml
COPY . .

CMD ["python3", "-m" , "telegram_bot.py"]
