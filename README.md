# 敦煌洞窟信息系统

管理莫高窟、榆林窟等洞窟信息的Web应用。

## 技术栈

- **前端**: React + Vite + TailwindCSS
- **后端**: FastAPI + SQLAlchemy
- **数据库**: MySQL
- **部署**: Docker Compose

## 快速开始

### 1. 初始化数据库

```bash
mysql -h 192.168.1.108 -u chenwei -p761211 -e "CREATE DATABASE IF NOT EXISTS dunhuang_grottoes CHARACTER SET utf8mb4;"
mysql -h 192.168.1.108 -u chenwei -p761211 dunhuang_grottoes < backend/init_db.sql
```

### 2. 启动服务

```bash
docker-compose up -d
```

### 3. 访问应用

- 前端: http://localhost:5104
- 后端API: http://localhost:5204
- 默认账号: admin / admin123

## 项目结构

```
├── backend/          # 后端服务 (FastAPI)
├── frontend/         # 前端服务 (React)
├── docker-compose.yml
└── README.md
```