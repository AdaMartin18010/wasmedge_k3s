# Docker 示例

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 理论基础](#11-理论基础)
- [2 Dockerfile 示例](#2-dockerfile-示例)
  - [2.1 基础 Dockerfile](#21-基础-dockerfile)
  - [2.2 多阶段构建示例](#22-多阶段构建示例)
  - [2.3 优化后的 Dockerfile](#23-优化后的-dockerfile)
- [3 docker-compose 示例](#3-docker-compose-示例)
  - [3.1 基础 docker-compose.yml](#31-基础-docker-composeyml)
  - [3.2 微服务 docker-compose.yml](#32-微服务-docker-composeyml)
- [4 容器运行示例](#4-容器运行示例)
  - [4.1 基础容器运行](#41-基础容器运行)
  - [4.2 带环境变量的容器运行](#42-带环境变量的容器运行)
  - [4.3 带卷挂载的容器运行](#43-带卷挂载的容器运行)
  - [4.4 带网络配置的容器运行](#44-带网络配置的容器运行)
- [5 相关文档](#5-相关文档)
  - [5.1 理论论证](#51-理论论证)
  - [5.2 架构视角](#52-架构视角)
  - [5.3 技术文档](#53-技术文档)

---

## 1 概述

本文档提供 **Docker 容器化的实际代码示例和配置示例**，包含可直接运行的
Dockerfile、docker-compose 配置和容器运行命令。

### 1.1 理论基础

Docker 容器化实现基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₂（容器化层）**：将 VM 抽象为轻量容器
- **引理 L1（容器干扰）**：容器间干扰可建模为线性时不变系统

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 Dockerfile 示例

### 2.1 基础 Dockerfile

```dockerfile
# 使用官方 Python 运行时作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["python", "app.py"]
```

### 2.2 多阶段构建示例

```dockerfile
# 第一阶段：构建阶段
FROM golang:1.21-alpine AS builder

WORKDIR /build

# 复制 go.mod 和 go.sum
COPY go.mod go.sum ./

# 下载依赖
RUN go mod download

# 复制源代码
COPY . .

# 构建应用
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# 第二阶段：运行阶段
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# 从构建阶段复制二进制文件
COPY --from=builder /build/app .

# 暴露端口
EXPOSE 8080

# 启动应用
CMD ["./app"]
```

### 2.3 优化后的 Dockerfile

```dockerfile
# 使用官方 Node.js 运行时作为基础镜像
FROM node:20-alpine AS base

# 设置工作目录
WORKDIR /app

# 安装依赖阶段
FROM base AS deps
COPY package*.json ./
RUN npm ci --only=production

# 构建阶段
FROM base AS build
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 运行阶段
FROM base AS runtime
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

---

## 3 docker-compose 示例

### 3.1 基础 docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3.2 微服务 docker-compose.yml

```yaml
version: "3.8"

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - api

  api:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 4 容器运行示例

### 4.1 基础容器运行

```bash
# 构建镜像
docker build -t myapp:v1.0 .

# 运行容器
docker run -d -p 8000:8000 --name myapp myapp:v1.0

# 查看容器日志
docker logs myapp

# 停止容器
docker stop myapp

# 删除容器
docker rm myapp
```

### 4.2 带环境变量的容器运行

```bash
# 使用环境变量文件
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  --name myapp \
  myapp:v1.0
```

### 4.3 带卷挂载的容器运行

```bash
# 挂载数据卷
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --name myapp \
  myapp:v1.0
```

### 4.4 带网络配置的容器运行

```bash
# 创建网络
docker network create mynetwork

# 在指定网络中运行容器
docker run -d \
  --network mynetwork \
  --name myapp \
  myapp:v1.0
```

---

## 5 相关文档

### 5.1 理论论证

- **`../../00-theory/02-induction-proof/psi2-containerization.md`** - 容器化层归
  纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理
- **`../../00-theory/05-lemmas-theorems/L1-container-interference.md`** - 容器干
  扰引理

### 5.2 架构视角

- **`../../02-views/10-quick-views/containerization-view.md`** - 容器化架构视角

### 5.3 技术文档

- **`../../../TECHNICAL/01-core-foundations/docker/docker.md`** - Docker 技术文
  档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
