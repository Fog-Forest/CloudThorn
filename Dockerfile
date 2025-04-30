FROM python:3.10-slim
LABEL authors="Kinoko"

# 设置工作目录
COPY ./app /app
WORKDIR /app

# Python库路径
ENV PYTHONPATH=/

# 安装 Chromium 浏览器及相关依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm-dev \
    libxkbcommon-dev \
    libgbm-dev \
    libasound2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64,arm64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]

# 暴露 FastAPI 应用的端口
EXPOSE 8675

# 设置用户为 root
USER root
