FROM python:3.8

WORKDIR ./wenjuanxing

ADD . .

RUN python -m pip install --upgrade pip
RUN sudo pip install -r requirements.txt

CMD ["python", "./main.py"]