# 学生信息管理系统

基于 Django + Vue 3 + SQLite 的学生信息管理系统，支持管理员/教师/学生三种角色。

## 技术栈

- **后端**: Django 5 + Django REST Framework + SQLite
- **前端**: Vue 3 + Vite + Element Plus + ECharts + Pinia

## 环境要求

- Python 3.10+
- Node.js 16+
- npm 8+

## 快速启动

### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 安装依赖（首次）
python -m pip install -r requirements.txt

# 数据库迁移（首次）
python manage.py migrate

# 生成测试数据（首次，可选）
python manage.py seed_data

# 启动服务
python manage.py runserver
```

后端运行在 `http://localhost:8000`

### 2. 启动前端

```bash
# 进入前端目录（新开一个终端）
cd frontend

# 安装依赖（首次）
npm install

# 启动服务
npm run dev
```

前端运行在 `http://localhost:5173`

### 3. 访问系统

打开浏览器访问 `http://localhost:5173`，使用以下账号登录：

| 角色 | 账号 | 密码 |
|------|------|------|
| 管理员 | admin | 123456 |
| 教师（计算机一班班主任） | T2022001 | 123456 |
| 教师（软件工程一班班主任） | T2022002 | 123456 |
| 教师（数据科学一班班主任） | T2023001 | 123456 |
| 教师（人工智能一班班主任） | T2023002 | 123456 |
| 学生（示例） | 202201001 | 123456 |

学生账号格式：`2022XXYYY`，XX 为班级编号（01-04），YYY 为序号（001-020）。
例如：202201001（计算机一班1号）、202202015（软件工程一班15号）、202203020（数据科学一班20号）。

## 功能说明

### 管理员

- 学生管理：增删改查、批量导入/导出 Excel
- 教师管理：增删改查、启用/禁用账号
- 班级管理：增删改查
- 课程管理：增删改查
- 成绩管理：按课程批量录入、查询、导出
- 信息审核：审核学生个人信息变更申请
- 数据统计：仪表盘图表
- 操作日志：查看系统操作记录

### 教师

- 管理自己班级的学生、课程、成绩
- 审核本班学生的信息变更申请

### 学生

- 查看个人信息和成绩
- 修改个人信息（需教师/管理员审核）

## 项目结构

```
stuMan/
├── backend/                # Django 后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── stuMan/             # 项目配置
│   └── apps/               # 应用模块
│       ├── users/          # 用户认证
│       ├── students/       # 学生管理
│       ├── teachers/       # 教师管理
│       ├── classes/        # 班级管理
│       ├── courses/        # 课程管理
│       ├── scores/         # 成绩管理
│       └── logs/           # 操作日志
│
├── frontend/               # Vue 前端
│   ├── src/
│   │   ├── api/            # 接口请求
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由
│   │   ├── store/          # 状态管理
│   │   └── utils/          # 工具函数
│   └── vite.config.js
│
└── docs/                   # 设计文档和实现计划
```

## 常见问题

**Q: 前端请求报错 403？**
确保后端已启动，且 `django-cors-headers` 已配置。

**Q: 忘记密码？**
在后端目录执行 `python manage.py seed_data` 会重置所有密码为 `123456`。

**Q: 想重新初始化数据？**
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py seed_data
```

**Q: 端口被占用？**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```
