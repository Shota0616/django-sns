FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
ENV WORKDIR /opt/app
WORKDIR ${WORKDIR}
# ログファイル作成
RUN mkdir -p /var/log/uwsgi/ && touch uwsgi.log
RUN mkdir -p /var/log/django/ && touch /var/log/django/info.log && touch /var/log/django/warning.log && touch /var/log/django/error.log
# pip install
COPY requirements.txt ${WORKDIR}
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# apt install
RUN apt update
RUN apt install -y vim
COPY . ${WORKDIR}
#コンテナ作成時に実行されるコマンド
# uwsgi起動
CMD ["uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]