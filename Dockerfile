FROM python:3.8

WORKDIR ./wenjuanxing

ADD . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U pip && pyppeteer-install

CMD ["python", "./main.py"]