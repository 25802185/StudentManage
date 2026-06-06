# 学生信息管理系统 - 设计文档

## 1. 项目概述

**项目名称**: 学生信息管理系统
**技术栈**: Django 5 + Vue 3 + SQLite + Element Plus
**目标**: 基于角色（管理员/教师/学生）的学生信息管理平台，支持学生信息管理、班级管理、课程管理、成绩管理、数据统计等功能。

---

## 2. 用户角色与权限

### 2.1 角色定义

| 角色 | 说明 |
|------|------|
| 管理员 | 系统最高权限，管理所有数据和用户 |
| 教师 | 管理自己所带班级的学生、课程和成绩 |
| 学生 | 查看自己的信息和成绩，可申请修改个人信息 |

### 2.2 权限矩阵

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

## 3. 数据模型

### 3.1 用户表 (User)

扩展 Django 内置 User 模型：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| username | CharField | 登录账号（学号/工号） |
| password | CharField | 密码（哈希存储） |
| role | CharField | 角色：admin / teacher / student |
| is_active | BooleanField | 是否启用 |
| created_at | DateTimeField | 创建时间 |

### 3.2 学生表 (Student)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| user | OneToOneField → User | 关联用户 |
| student_no | CharField | 学号（唯一） |
| name | CharField | 姓名 |
| gender | CharField | 性别 |
| age | IntegerField | 年龄 |
| class_ref | ForeignKey → Class | 所属班级 |
| phone | CharField | 联系电话 |
| email | EmailField | 邮箱 |
| address | CharField | 家庭地址 |
| avatar | ImageField | 头像（可选） |
| status | CharField | 正常/待审核/审核驳回 |

### 3.3 教师表 (Teacher)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| user | OneToOneField → User | 关联用户 |
| teacher_no | CharField | 工号（唯一） |
| name | CharField | 姓名 |
| gender | CharField | 性别 |
| title | CharField | 职称 |
| phone | CharField | 联系电话 |
| email | EmailField | 邮箱 |
| class_ref | ForeignKey → Class | 所带班级 |

### 3.4 班级表 (Class)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| name | CharField | 班级名称 |
| grade | CharField | 年级 |
| major | CharField | 专业 |
| teacher | ForeignKey → Teacher | 班主任 |
| student_count | IntegerField | 学生人数（冗余字段） |
| created_at | DateTimeField | 创建时间 |

### 3.5 课程表 (Course)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| name | CharField | 课程名称 |
| credit | FloatField | 学分 |
| class_ref | ForeignKey → Class | 所属班级 |
| teacher | ForeignKey → Teacher | 授课教师 |
| description | TextField | 课程描述（可选） |
| created_at | DateTimeField | 创建时间 |

### 3.6 成绩表 (Score)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| student | ForeignKey → Student | 学生 |
| course | ForeignKey → Course | 课程 |
| score | FloatField | 成绩 |
| semester | CharField | 学期（如 2025-2026-1） |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

联合唯一约束: (student, course, semester)

### 3.7 信息变更审核表 (InfoChangeRequest)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| student | ForeignKey → Student | 学生 |
| field_name | CharField | 修改的字段名 |
| old_value | CharField | 原值 |
| new_value | CharField | 新值 |
| status | CharField | pending / approved / rejected |
| reviewer | ForeignKey → User | 审核人 |
| review_time | DateTimeField | 审核时间 |
| remark | CharField | 审核备注 |
| created_at | DateTimeField | 申请时间 |

### 3.8 操作日志表 (OperationLog)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| user | ForeignKey → User | 操作人 |
| action | CharField | 操作类型 |
| target | CharField | 操作对象 |
| detail | TextField | 操作详情 |
| ip_address | CharField | IP 地址 |
| created_at | DateTimeField | 操作时间 |

---

## 4. 功能模块详细设计

### 4.1 登录认证与权限管理

**登录流程**:
1. 用户输入账号（学号/工号）和密码
2. 后端验证身份，返回角色信息
3. 前端根据角色动态渲染菜单和路由

**权限控制**:
- 后端: 基于 DRF 的权限类，自定义 `IsAdmin`, `IsTeacher`, `IsStudent` 权限
- 前端: 路由守卫 + 动态菜单生成

**密码管理**:
- 学生/教师首次登录默认密码为学号/工号后6位
- 支持修改密码（需验证旧密码）

### 4.2 学生信息管理

**管理员/教师操作**:
- 查看学生列表（支持按班级、姓名、学号筛选）
- 新增学生（自动创建关联用户账号）
- 编辑学生信息
- 删除学生
- 批量导入学生（Excel 上传）

**学生自助**:
- 查看个人信息
- 修改个人信息 → 提交后状态变为「待审核」
- 查看审核记录

**审核流程**:
1. 学生提交修改申请 → 生成 InfoChangeRequest 记录
2. 教师/管理员在审核列表中查看待审核项
3. 通过 → 更新 Student 表对应字段
4. 驳回 → 记录驳回原因，学生可查看

### 4.3 教师信息管理（管理员）

- 教师列表（搜索/筛选）
- 新增教师（自动创建用户账号）
- 编辑教师信息
- 删除教师
- 启用/禁用教师账号

### 4.4 班级管理（管理员）

- 班级列表
- 新增班级（指定班级名称、年级、专业、班主任）
- 编辑/删除班级
- 查看班级详情（含学生名单）

### 4.5 课程与成绩管理

**课程管理**:
- 课程列表（管理员看全部，教师看本班）
- 新增/编辑/删除课程
- 指定授课教师和所属班级

**成绩管理**:
- 按课程录入成绩（批量录入界面，表格形式）
- 修改已有成绩
- 学生端查看自己的成绩列表 + 计算总绩点
- 教师/管理员按课程查看成绩统计

### 4.6 数据统计与导出

**管理员首页仪表盘**:
- 学生总数、教师总数、班级数、课程数（卡片展示）
- 近期操作日志

**图表统计**:
- 成绩分布柱状图（按课程）
- 各班级学生人数对比图
- 成绩等级分布饼图（优秀/良好/中等/及格/不及格）

**Excel 导出**:
- 学生信息导出
- 成绩列表导出

### 4.7 操作日志（管理员）

- 自动记录：登录、信息修改、成绩录入、审核等操作
- 日志列表（按时间倒序，支持按操作类型筛选）
- 查看操作详情

---

## 5. API 接口设计

统一前缀 `/api/`，RESTful 风格。

### 5.1 认证模块

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login/` | 登录 |
| POST | `/api/auth/logout/` | 登出 |
| GET | `/api/auth/userinfo/` | 获取当前用户信息 |
| PUT | `/api/auth/password/` | 修改密码 |

### 5.2 学生管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/students/` | 学生列表（支持筛选/搜索/分页） |
| POST | `/api/students/` | 新增学生 |
| GET | `/api/students/{id}/` | 学生详情 |
| PUT | `/api/students/{id}/` | 编辑学生 |
| DELETE | `/api/students/{id}/` | 删除学生 |
| POST | `/api/students/import/` | 批量导入（Excel） |
| GET | `/api/students/export/` | 导出 Excel |

### 5.3 教师管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/teachers/` | 教师列表 |
| POST | `/api/teachers/` | 新增教师 |
| GET | `/api/teachers/{id}/` | 教师详情 |
| PUT | `/api/teachers/{id}/` | 编辑教师 |
| DELETE | `/api/teachers/{id}/` | 删除教师 |
| PUT | `/api/teachers/{id}/toggle/` | 启用/禁用 |

### 5.4 班级管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/classes/` | 班级列表 |
| POST | `/api/classes/` | 新增班级 |
| GET | `/api/classes/{id}/` | 班级详情 |
| PUT | `/api/classes/{id}/` | 编辑班级 |
| DELETE | `/api/classes/{id}/` | 删除班级 |

### 5.5 课程管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/courses/` | 课程列表 |
| POST | `/api/courses/` | 新增课程 |
| GET | `/api/courses/{id}/` | 课程详情 |
| PUT | `/api/courses/{id}/` | 编辑课程 |
| DELETE | `/api/courses/{id}/` | 删除课程 |

### 5.6 成绩管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/scores/` | 成绩列表 |
| POST | `/api/scores/` | 新增成绩 |
| PUT | `/api/scores/{id}/` | 修改成绩 |
| DELETE | `/api/scores/{id}/` | 删除成绩 |
| POST | `/api/scores/batch/` | 批量录入成绩 |
| GET | `/api/scores/export/` | 导出成绩 Excel |

### 5.7 信息审核

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/info-changes/` | 审核列表 |
| POST | `/api/info-changes/` | 学生提交修改申请 |
| PUT | `/api/info-changes/{id}/approve/` | 审核通过 |
| PUT | `/api/info-changes/{id}/reject/` | 审核驳回 |

### 5.8 数据统计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats/dashboard/` | 仪表盘数据 |
| GET | `/api/stats/score-distribution/` | 成绩分布统计 |
| GET | `/api/stats/class-students/` | 班级人数统计 |

### 5.9 操作日志

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/logs/` | 日志列表 |

---

## 6. 前端页面设计

### 6.1 布局

- 左侧菜单栏 + 顶部导航栏 + 右侧内容区
- 菜单根据角色动态生成
- 响应式布局

### 6.2 页面清单

| 页面 | 说明 | 可见角色 |
|------|------|---------|
| 登录页 | 账号密码登录 | 全部 |
| 首页/仪表盘 | 数据概览 + 图表 | 管理员/教师 |
| 学生列表 | 搜索/筛选/CRUD/导入导出 | 管理员/教师 |
| 学生详情 | 查看/编辑学生信息 | 管理员/教师/学生(自己) |
| 教师列表 | 搜索/CRUD | 管理员 |
| 班级列表 | CRUD + 学生名单 | 管理员 |
| 课程列表 | CRUD | 管理员/教师 |
| 成绩录入 | 按课程批量录入表格 | 管理员/教师 |
| 成绩查询 | 成绩列表/统计 | 全部 |
| 信息审核 | 待审核列表 + 审核操作 | 管理员/教师 |
| 我的申请 | 学生查看自己的审核记录 | 学生 |
| 个人信息 | 查看/修改个人信息 | 全部 |
| 修改密码 | 修改登录密码 | 全部 |
| 操作日志 | 日志列表 | 管理员 |

---

## 7. 技术实现要点

### 7.1 后端

- Django REST Framework 构建 API
- 自定义权限类实现角色控制
- Django Signal 记录操作日志
- openpyxl 实现 Excel 导入导出
- django-filter 实现筛选

### 7.2 前端

- Vue Router 路由守卫 + 动态路由
- Axios 封装请求拦截器（自动携带 token）
- Element Plus 组件库
- ECharts 图表展示
- Pinia 状态管理

### 7.3 数据库

- SQLite（开发阶段）
- Django ORM 管理模型
- 数据库迁移通过 makemigrations / migrate
