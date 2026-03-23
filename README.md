# Library-All 项目使用与部署文档

## 项目简介

Library-All 是一个图书馆管理系统，包含前端（Vue.js）和后端（FastAPI），数据库采用 MySQL 8.1。支持图书管理、借阅管理、预约管理、通知管理和建议管理等功能。

---

## 目录结构说明

```
library-all/
  ├── backend/         		# 后端 FastAPI 服务
  ├── frontend/        		# 前端 Vue.js 项目
  ├── library-all-data.sql  # 数据库初始化 SQL 脚本
  └── ...              		# 其他文档和配置文件
```

---

## 环境要求

- Node.js ≥ 14.x
- npm ≥ 6.x
- Python ≥ 3.8
- MySQL ≥ 5.7

---

## 环境准备

### 1. 安装 Node.js 和 npm（前端需要）

- 打开 [Node.js 官网](https://nodejs.org/zh-cn)
- 下载 LTS 版本（推荐），并一路“下一步”安装
- 安装完成后，打开命令提示符（Win+R 输入 cmd 回车），输入：
  ```
  node -v
  npm -v
  ```
  能看到版本号即安装成功

### 2. 安装 Python（后端需要）

- 打开 [Python 官网](https://www.python.org/downloads/)
- 下载 Python 3.8 或更高版本，安装时务必勾选“Add Python to PATH”
- 安装完成后，命令行输入：
  ```
  python --version
  ```
  能看到版本号即安装成功

### 3. 安装 MySQL（数据库）

- 打开 [MySQL 官网](https://dev.mysql.com/downloads/installer/)
- 下载并安装 MySQL Community 版本，记住设置的 root 密码
- 安装完成后，打开“命令行客户端”或用图形界面（如 MySQL Workbench、navicat）

---

## 一、数据库部署

1. 安装 MySQL 并启动服务。
2. 创建数据库（如：library_all），并导入初始化数据：

```bash
mysql -u root -p
# 输入密码后执行
CREATE DATABASE library_all DEFAULT CHARACTER SET utf8mb4;
USE library_all;
SOURCE /path/to/library-all.sql;
```

---

## 二、后端部署（FastAPI）

1. 进入 backend 目录，创建虚拟环境并激活：

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

> 如果没有 requirements.txt，请手动安装主要依赖：
> 
> ```
> pip install fastapi uvicorn pymysql python-jose
> ```

3. 配置数据库连接（如有 config 文件请修改，否则在 main.py/database.py 中修改数据库连接参数）。

4. 启动后端服务：

```bash
python main.py
```

---

## 三、前端部署（Vue.js）

1. 进入 frontend 目录：

```bash
cd frontend
```

2. 安装依赖：

```bash
npm install
```

3. 启动前端开发服务器（端口为 8080）：

```bash
npm run serve
```

4. 访问前端页面：

在浏览器中打开 [http://localhost:8080](http://localhost:8080)

---

## 四、常见问题

- 数据库连接失败：请检查 backend 的数据库配置、MySQL 是否启动、端口和用户名密码是否正确。
- 前端无法访问后端：请确保后端已启动，且前后端接口地址一致（可在 frontend/src 下查找和修改 API 地址）。
- 依赖安装失败：请检查 Node.js、npm、Python 版本，或尝试使用国内镜像源。

---

如有其他问题，欢迎随时咨询（vx：ncwzdlsd）！
