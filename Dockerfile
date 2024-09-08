# 使用官方Python运行时作为父镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到位于/app中的容器中
COPY . /app

# 复制requirements.txt到容器内
COPY requirements.txt /tmp/requirements.txt

# 安装依赖
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_ENV=production

# 使用gunicorn启动Flask应用
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5000", "run:app"]