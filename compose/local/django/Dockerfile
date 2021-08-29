ARG PYTHON_VERSION=3.9-slim-buster

# SQL Server Command Line Tools
FROM python:${PYTHON_VERSION} as python


FROM python as python-build-stage


ARG BUILD_ENVIRONMENT=local

# apt-get and system utilities
RUN apt-get update && apt-get install --no-install-recommends -y \
	curl apt-transport-https debconf-utils curl wget gnupg  netcat \
    build-essential \
	python3 \
    python3-pip \
    python3-dev \
    musl-dev \
    unixodbc \
    unixodbc-dev \
    && apt-get -y autoclean \
    && apt-get -y autoremove  \
    && rm -rf /var/lib/apt/lists/*
    


# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers and tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN /bin/bash -c "source ~/.bashrc"
RUN apt-get --assume-yes install freetds-dev freetds-bin
RUN apt-get --assume-yes install python-dev



RUN apt-get -y install locales
RUN locale-gen en_US.UTF-8

COPY ./requirements .

# install dependencies
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt



# Python 'run' stage

FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}


RUN apt-get update && apt-get install --no-install-recommends -y \
    curl apt-transport-https debconf-utils curl wget gnupg  netcat \
    python3 \
    python3-pip \
    python3-dev \
    musl-dev \
    unixodbc \
    unixodbc-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
    
# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers and tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN /bin/bash -c "source ~/.bashrc"

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower





COPY . &{APP_HOME}

# copy entrypoint.sh

ENTRYPOINT ["/entrypoint"]