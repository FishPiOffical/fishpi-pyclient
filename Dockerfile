
FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    tzdata \
    && rm -rf /var/cache/apk/*
ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime

COPY src/ src/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python", "-m", "src.main"]