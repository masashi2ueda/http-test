FROM python:3.10

ARG UID
ARG GID
ARG USERNAME
ARG GROUPNAME
RUN groupadd -g ${GID} ${GROUPNAME} -f && \
    useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME}

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

USER ${USERNAME}
WORKDIR /src