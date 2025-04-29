FROM python:3.10-slim
LABEL authors="Kinoko"

# 设置工作目录
COPY ./app /app
WORKDIR /app

# Python库路径
ENV PYTHONPATH=/

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]

# 暴露 FastAPI 应用的端口
EXPOSE 8675

# 设置用户为 root
USER root
