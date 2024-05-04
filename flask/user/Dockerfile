FROM python:3.10

# コンテナ内で作成されたファイルをホストでも操作できるようにする
ARG UID
ARG GID
ARG USERNAME
ARG GROUPNAME
RUN groupadd -g ${GID} ${GROUPNAME} -f && \
    useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME}

# python環境の設定
RUN apt-get update
USER ${USERNAME}
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install locust

# 計測実行
WORKDIR /src