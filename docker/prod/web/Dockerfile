FROM python:3.6.6
MAINTAINER ramaniuk@localhost

COPY . /debitrum

WORKDIR /debitrum

RUN pip install -r requirements_prod.txt

COPY ./docker/prod/web/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]