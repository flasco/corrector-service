FROM python:3.7 AS downloader
WORKDIR /usr/local

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list &&  \
    sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list &&  \
    apt-get update && \
    apt install -y git git-lfs && \
    git lfs install && \
    git clone https://huggingface.co/shibing624/macbert4csc-base-chinese model

FROM python:3.7

COPY ./ /usr/local/flask_app/

WORKDIR /usr/local/flask_app/

COPY --from=downloader /usr/local/model ./model

# 设置工作目录，容器运行时，命令行默认就在这个目录

ARG PYTORCH='1.12.0'

ENV FLASK_APP_ENV='production'

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "wsgi.py"]