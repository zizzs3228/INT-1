FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=example
ENV MYSQL_DATABASE=testdb
ENV MYSQL_USER=testuser
ENV MYSQL_PASSWORD=testpassword

COPY init.sql /docker-entrypoint-initdb.d/
