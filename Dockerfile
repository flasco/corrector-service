FROM python:3.10.4 AS downloader
WORKDIR /usr/local

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list &&  \
    sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list &&  \
    apt-get update && \
    apt install -y git git-lfs && \
    git lfs install && \
    git clone --depth=1 https://huggingface.co/shibing624/macbert4csc-base-chinese model && \
    cd model && rm -rf .git

FROM python:3.10.4

COPY ./ /usr/local/flask_app/

WORKDIR /usr/local/flask_app/

COPY --from=downloader /usr/local/model ./model

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV FLASK_APP_ENV='production'

CMD ["python", "wsgi.py"]