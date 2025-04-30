FROM python:3.10-slim
LABEL authors="Kinoko"

# 设置工作目录
COPY ./app /app
WORKDIR /app

# 设置 Python 库路径
ENV PYTHONPATH=/

# 安装 Chromium 浏览器及相关依赖
RUN apt-get update \
    && apt-get install -y wget gnupg libnss3 libatk-bridge2.0-0 libdrm-dev libxkbcommon-dev libgbm-dev libasound2 xvfb \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && ARCH=$(dpkg --print-architecture) \
    && sh -c "echo \"deb [arch=$ARCH] http://dl.google.com/linux/chrome/deb/ stable main\" >> /etc/apt/sources.list.d/google.list" \
    && apt-get update \
    && apt-get install -y chromium \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \

# 启动虚拟 X 服务器，用以支持图形化应用运行
# -s 参数指定虚拟屏幕的设置，这里设置分辨率为 1280x720，色彩深度为 16 位
# ENTRYPOINT ["xvfb-run", "-s", "-screen 0 1280x720x16", "python", "main.py"]
ENTRYPOINT ["python", "main.py"]

# 暴露 FastAPI 应用的端口
EXPOSE 8675

# 设置用户为 root
USER root
