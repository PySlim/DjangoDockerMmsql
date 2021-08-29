FROM mcr.microsoft.com/mssql/server:2019-CU3-ubuntu-18.04

COPY ./compose/production/sql/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
