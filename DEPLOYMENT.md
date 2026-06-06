# 学生信息管理系统 - 项目部署文档

## 项目概述

- **项目名称**: 学生信息管理系统
- **技术栈**: Django 5.x + Vue 3 + SQLite
- **前端**: Vue 3 + Vite + Element Plus + Axios
- **后端**: Django 5 + Django REST Framework
- **数据库**: SQLite（Django 默认）

---

## 环境要求

| 软件 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.10+ | Django 运行环境 |
| Node.js | 18+ | Vue 前端构建 |
| npm | 9+ | 前端包管理 |
| pip | 最新 | Python 包管理 |

---

## 功能模块

### 角色定义

| 角色 | 说明 |
|------|------|
| 管理员 | 系统最高权限，管理所有数据和用户 |
| 教师 | 管理自己所带班级的学生、课程和成绩 |
| 学生 | 查看自己的信息和成绩，可申请修改个人信息（需审核） |

### 功能清单

| 序号 | 模块 | 说明 |
|------|------|------|
| 1 | 登录认证与权限管理 | 三种角色登录、动态菜单、密码管理 |
| 2 | 学生信息管理 | CRUD、搜索筛选、Excel 导入导出、自助修改（需审核） |
| 3 | 教师信息管理 | CRUD、账号启用/禁用（管理员） |
| 4 | 班级管理 | CRUD、学生人数统计（管理员） |
| 5 | 课程与成绩管理 | 课程 CRUD、成绩批量录入、成绩查询、绩点计算 |
| 6 | 数据统计与导出 | 仪表盘、图表统计、Excel 导出 |
| 7 | 操作日志 | 记录关键操作，管理员可查 |

### 权限矩阵

| 功能 | 管理员 | 教师 | 学生 |
|------|:------:|:----:|:----:|
| 管理教师账号 | ✅ | ❌ | ❌ |
| 管理学生账号 | ✅ | ✅（本班） | ❌ |
| 管理班级 | ✅ | ❌ | ❌ |
| 管理课程 | ✅ | ✅（本班） | ❌ |
| 录入/修改成绩 | ✅ | ✅（本班） | ❌ |
| 查看成绩 | ✅ | ✅（本班） | ✅（自己） |
| 修改个人信息 | ✅ | ✅ | ✅（需审核） |
| 审核学生信息变更 | ✅ | ✅（本班） | ❌ |
| 数据统计/导出 | ✅ | ✅（本班） | ❌ |
| 操作日志 | ✅ | ❌ | ❌ |

---

## 项目结构

```
stuMan/
├── backend/                # Django 后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── stuMan/             # Django 项目配置
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/          # 用户认证模块
│   │   ├── students/       # 学生管理模块
│   │   ├── teachers/       # 教师管理模块
│   │   ├── classes/        # 班级管理模块
│   │   ├── courses/        # 课程管理模块
│   │   ├── scores/         # 成绩管理模块
│   │   └── logs/           # 操作日志模块
│   └── db.sqlite3          # SQLite 数据库（自动生成）
│
├── frontend/               # Vue 前端
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── api/            # 接口请求
│   │   ├── views/          # 页面组件
│   │   │   ├── auth/       # 登录、个人信息
│   │   │   ├── dashboard/  # 仪表盘
│   │   │   ├── students/   # 学生管理
│   │   │   ├── teachers/   # 教师管理
│   │   │   ├── classes/    # 班级管理
│   │   │   ├── courses/    # 课程管理
│   │   │   ├── scores/     # 成绩管理
│   │   │   └── logs/       # 操作日志
│   │   ├── components/     # 公共组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # 状态管理（Pinia）
│   │   └── utils/          # 工具函数
│   └── public/
│
├── docs/                   # 设计文档
├── DEPLOYMENT.md           # 本文档
└── README.md
```

---

## 后端部署（Django）

### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

```
django>=5.0
djangorestframework>=3.14
django-cors-headers>=4.3
django-filter>=23.5
openpyxl>=3.1          # Excel 导入导出
Pillow>=10.0           # 头像图片处理（可选）
```

### 3. 初始化数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建管理员账号

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

### 5. 启动后端服务

```bash
python manage.py runserver 0.0.0.0:8000
```

后端运行在 `http://localhost:8000`

---

## 前端部署（Vue）

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 开发模式运行

```bash
npm run dev
```

前端运行在 `http://localhost:5173`

### 3. 生产环境构建

```bash
npm run build
```

构建产物输出到 `frontend/dist/` 目录。

---

## 关键配置

### Django settings.py 要点

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'django_filters',
    'apps.users',
    'apps.students',
    'apps.teachers',
    'apps.classes',
    'apps.courses',
    'apps.scores',
    'apps.logs',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 放在最前面
    ...
]

# 允许前端跨域（开发环境）
CORS_ALLOW_ALL_ORIGINS = True

# DRF 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Vue vite.config.js 要点

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

---

## 接口规范

采用 RESTful 风格，统一前缀 `/api/`：

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 认证 | POST | `/api/auth/login/` | 登录 |
| | POST | `/api/auth/logout/` | 登出 |
| | GET | `/api/auth/userinfo/` | 当前用户信息 |
| | PUT | `/api/auth/password/` | 修改密码 |
| 学生 | GET | `/api/students/` | 学生列表（筛选/搜索/分页） |
| | POST | `/api/students/` | 新增学生 |
| | GET/PUT/DELETE | `/api/students/{id}/` | 详情 / 编辑 / 删除 |
| | POST | `/api/students/import/` | 批量导入 Excel |
| | GET | `/api/students/export/` | 导出 Excel |
| 教师 | GET | `/api/teachers/` | 教师列表 |
| | POST | `/api/teachers/` | 新增教师 |
| | GET/PUT/DELETE | `/api/teachers/{id}/` | 详情 / 编辑 / 删除 |
| | PUT | `/api/teachers/{id}/toggle/` | 启用/禁用 |
| 班级 | GET | `/api/classes/` | 班级列表 |
| | POST | `/api/classes/` | 新增班级 |
| | GET/PUT/DELETE | `/api/classes/{id}/` | 详情 / 编辑 / 删除 |
| 课程 | GET | `/api/courses/` | 课程列表 |
| | POST | `/api/courses/` | 新增课程 |
| | GET/PUT/DELETE | `/api/courses/{id}/` | 详情 / 编辑 / 删除 |
| 成绩 | GET | `/api/scores/` | 成绩列表 |
| | POST | `/api/scores/` | 新增成绩 |
| | PUT/DELETE | `/api/scores/{id}/` | 修改 / 删除 |
| | POST | `/api/scores/batch/` | 批量录入 |
| | GET | `/api/scores/export/` | 导出 Excel |
| 审核 | GET | `/api/info-changes/` | 审核列表 |
| | POST | `/api/info-changes/` | 学生提交修改申请 |
| | PUT | `/api/info-changes/{id}/approve/` | 审核通过 |
| | PUT | `/api/info-changes/{id}/reject/` | 审核驳回 |
| 统计 | GET | `/api/stats/dashboard/` | 仪表盘数据 |
| | GET | `/api/stats/score-distribution/` | 成绩分布 |
| | GET | `/api/stats/class-students/` | 班级人数 |
| 日志 | GET | `/api/logs/` | 操作日志列表 |

---

## 常见问题

### Q: 前端请求 403 Forbidden
确保 `django-cors-headers` 已安装并配置 `CORS_ALLOW_ALL_ORIGINS = True`。

### Q: 数据库文件在哪里
SQLite 数据库文件位于 `backend/db.sqlite3`，迁移后自动生成，无需额外安装数据库服务。

### Q: 如何重置数据库
```bash
rm backend/db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Q: 端口被占用
```bash
# Windows 查看占用端口的进程
netstat -ano | findstr :8000

# 杀掉进程（替换 PID）
taskkill /PID <PID> /F
```
