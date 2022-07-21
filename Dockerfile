FROM python:3.7
COPY ./ /usr/local/flask_app/

# 设置工作目录，容器运行时，命令行默认就在这个目录
WORKDIR /usr/local/flask_app/

# apt-get 更换国内源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list &&  \
    sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list &&  \
    apt-get update

ARG PYTORCH='1.12.0'

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt install -y git git-lfs

RUN git lfs install

RUN git clone https://huggingface.co/shibing624/macbert4csc-base-chinese model

CMD ["python", "wsgi.py"]