FROM postgres:9.5.25-alpine
COPY eel-psql.sql /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*
