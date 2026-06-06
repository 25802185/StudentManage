# 学生信息管理系统 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Django + Vue 3 + SQLite 的学生信息管理系统，支持管理员/教师/学生三种角色。

**Architecture:** 前后端分离架构。后端 Django REST Framework 提供 RESTful API，前端 Vue 3 + Element Plus 构建 SPA。通过 Session 认证，自定义权限类控制角色访问。

**Tech Stack:** Django 5, DRF, Vue 3, Vite, Element Plus, Pinia, ECharts, openpyxl, SQLite

---

## 文件结构总览

```
stuMan/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── stuMan/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── apps/
│       ├── __init__.py
│       ├── users/
│       │   ├── __init__.py
│       │   ├── models.py          # 自定义 User 模型
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── permissions.py     # 自定义权限类
│       │   └── admin.py
│       ├── students/
│       │   ├── __init__.py
│       │   ├── models.py          # Student, InfoChangeRequest
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── filters.py
│       │   └── admin.py
│       ├── teachers/
│       │   ├── __init__.py
│       │   ├── models.py          # Teacher
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   └── admin.py
│       ├── classes/
│       │   ├── __init__.py
│       │   ├── models.py          # Class
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   └── admin.py
│       ├── courses/
│       │   ├── __init__.py
│       │   ├── models.py          # Course
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   └── admin.py
│       ├── scores/
│       │   ├── __init__.py
│       │   ├── models.py          # Score
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   └── admin.py
│       └── logs/
│           ├── __init__.py
│           ├── models.py          # OperationLog
│           ├── serializers.py
│           ├── views.py
│           ├── urls.py
│           └── admin.py
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.js
        ├── App.vue
        ├── api/
        │   ├── index.js           # Axios 实例
        │   ├── auth.js
        │   ├── students.js
        │   ├── teachers.js
        │   ├── classes.js
        │   ├── courses.js
        │   ├── scores.js
        │   └── stats.js
        ├── router/
        │   └── index.js
        ├── store/
        │   └── user.js            # Pinia 用户状态
        ├── utils/
        │   └── permission.js      # 角色菜单配置
        └── views/
            ├── Login.vue
            ├── Layout.vue
            ├── Dashboard.vue
            ├── Profile.vue
            ├── ChangePassword.vue
            ├── students/
            │   ├── StudentList.vue
            │   └── StudentDetail.vue
            ├── teachers/
            │   └── TeacherList.vue
            ├── classes/
            │   └── ClassList.vue
            ├── courses/
            │   └── CourseList.vue
            ├── scores/
            │   ├── ScoreEntry.vue
            │   └── ScoreList.vue
            ├── info-changes/
            │   ├── InfoChangeList.vue
            │   └── MyApplications.vue
            └── logs/
                └── LogList.vue
```

---

## Phase 1: Django 项目基础

### Task 1: 创建 Django 项目和依赖

- [ ] **Step 1: 创建 Django 项目**

```bash
cd E:/personPro/stuMan
mkdir backend && cd backend
pip install django djangorestframework django-cors-headers django-filter openpyxl Pillow
django-admin startproject stuMan .
python manage.py startapp users
mkdir apps
mv users apps/
```

- [ ] **Step 2: 编写 requirements.txt**

创建 `backend/requirements.txt`:

```
django>=5.0
djangorestframework>=3.14
django-cors-headers>=4.3
django-filter>=23.5
openpyxl>=3.1
Pillow>=10.0
```

- [ ] **Step 3: 创建 apps 包**

创建 `backend/apps/__init__.py`（空文件）。

- [ ] **Step 4: 修改 settings.py**

修改 `backend/stuMan/settings.py`:

```python
import os
import sys

# 将 apps 目录加入 Python 路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方
    'rest_framework',
    'corsheaders',
    'django_filters',
    # 本地应用
    'apps.users',
    'apps.students',
    'apps.teachers',
    'apps.classes',
    'apps.courses',
    'apps.scores',
    'apps.logs',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# 跨域
CORS_ALLOW_ALL_ORIGINS = True

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# 媒体文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

- [ ] **Step 5: 创建其他 app 骨架**

```bash
cd E:/personPro/stuMan/backend
python manage.py startapp students && mv students apps/
python manage.py startapp teachers && mv teachers apps/
python manage.py startapp classes && mv classes apps/
python manage.py startapp courses && mv courses apps/
python manage.py startapp scores && mv scores apps/
python manage.py startapp logs && mv logs apps/
```

每个 app 的 `apps.py` 中修改 `name` 为 `apps.xxx`，例如 `apps/students/apps.py`:

```python
from django.apps import AppConfig

class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.students'
```

- [ ] **Step 6: 提交**

```bash
cd E:/personPro/stuMan
git add .
git commit -m "feat: initialize Django project with all app scaffolds"
```

---

### Task 2: 自定义 User 模型和权限

**Files:**
- Create: `backend/apps/users/models.py`
- Create: `backend/apps/users/permissions.py`
- Create: `backend/apps/users/serializers.py`
- Create: `backend/apps/users/admin.py`

- [ ] **Step 1: 编写 User 模型**

替换 `backend/apps/users/models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    ]
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
```

- [ ] **Step 2: 编写权限类**

创建 `backend/apps/users/permissions.py`:

```python
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin', 'teacher')
```

- [ ] **Step 3: 编写 User 序列化器**

替换 `backend/apps/users/serializers.py`:

```python
from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
```

- [ ] **Step 4: 配置 admin**

替换 `backend/apps/users/admin.py`:

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('role',)}),
    )
```

- [ ] **Step 5: 提交**

```bash
git add backend/apps/users/
git commit -m "feat: add custom User model and role permissions"
```

---

### Task 3: 数据模型（学生/教师/班级/课程/成绩/日志）

**Files:**
- Modify: `backend/apps/classes/models.py`
- Modify: `backend/apps/teachers/models.py`
- Modify: `backend/apps/students/models.py`
- Modify: `backend/apps/courses/models.py`
- Modify: `backend/apps/scores/models.py`
- Modify: `backend/apps/logs/models.py`

- [ ] **Step 1: 班级模型**

替换 `backend/apps/classes/models.py`:

```python
from django.db import models


class ClassInfo(models.Model):
    name = models.CharField('班级名称', max_length=50)
    grade = models.CharField('年级', max_length=20)
    major = models.CharField('专业', max_length=50)
    student_count = models.IntegerField('学生人数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'classes'
        verbose_name = '班级'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

- [ ] **Step 2: 教师模型**

替换 `backend/apps/teachers/models.py`:

```python
from django.db import models
from apps.users.models import User
from apps.classes.models import ClassInfo


class Teacher(models.Model):
    GENDER_CHOICES = [('male', '男'), ('female', '女')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_no = models.CharField('工号', max_length=20, unique=True)
    name = models.CharField('姓名', max_length=20)
    gender = models.CharField('性别', max_length=6, choices=GENDER_CHOICES)
    title = models.CharField('职称', max_length=20, blank=True, default='')
    phone = models.CharField('联系电话', max_length=20, blank=True, default='')
    email = models.EmailField('邮箱', blank=True, default='')
    class_ref = models.ForeignKey(
        ClassInfo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='teachers', verbose_name='所带班级'
    )

    class Meta:
        db_table = 'teachers'
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.teacher_no})'
```

- [ ] **Step 3: 学生模型**

替换 `backend/apps/students/models.py`:

```python
from django.db import models
from apps.users.models import User
from apps.classes.models import ClassInfo


class Student(models.Model):
    GENDER_CHOICES = [('male', '男'), ('female', '女')]
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('pending', '待审核'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_no = models.CharField('学号', max_length=20, unique=True)
    name = models.CharField('姓名', max_length=20)
    gender = models.CharField('性别', max_length=6, choices=GENDER_CHOICES)
    age = models.IntegerField('年龄', null=True, blank=True)
    class_ref = models.ForeignKey(
        ClassInfo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='students', verbose_name='所属班级'
    )
    phone = models.CharField('联系电话', max_length=20, blank=True, default='')
    email = models.EmailField('邮箱', blank=True, default='')
    address = models.CharField('家庭地址', max_length=200, blank=True, default='')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='normal')

    class Meta:
        db_table = 'students'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} ({self.student_no})'


class InfoChangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='change_requests')
    field_name = models.CharField('修改字段', max_length=50)
    old_value = models.CharField('原值', max_length=200)
    new_value = models.CharField('新值', max_length=200)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_changes', verbose_name='审核人'
    )
    review_time = models.DateTimeField('审核时间', null=True, blank=True)
    remark = models.CharField('审核备注', max_length=200, blank=True, default='')
    created_at = models.DateTimeField('申请时间', auto_now_add=True)

    class Meta:
        db_table = 'info_change_requests'
        verbose_name = '信息变更申请'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.name} - {self.field_name}'
```

- [ ] **Step 4: 课程模型**

替换 `backend/apps/courses/models.py`:

```python
from django.db import models
from apps.classes.models import ClassInfo
from apps.teachers.models import Teacher


class Course(models.Model):
    name = models.CharField('课程名称', max_length=50)
    credit = models.FloatField('学分')
    class_ref = models.ForeignKey(
        ClassInfo, on_delete=models.CASCADE, related_name='courses', verbose_name='所属班级'
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='courses', verbose_name='授课教师'
    )
    description = models.TextField('课程描述', blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
```

- [ ] **Step 5: 成绩模型**

替换 `backend/apps/scores/models.py`:

```python
from django.db import models
from apps.students.models import Student
from apps.courses.models import Course


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='scores')
    score = models.FloatField('成绩')
    semester = models.CharField('学期', max_length=20)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'scores'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name
        unique_together = ['student', 'course', 'semester']

    def __str__(self):
        return f'{self.student.name} - {self.course.name}: {self.score}'
```

- [ ] **Step 6: 操作日志模型**

替换 `backend/apps/logs/models.py`:

```python
from django.db import models
from apps.users.models import User


class OperationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs')
    action = models.CharField('操作类型', max_length=50)
    target = models.CharField('操作对象', max_length=100)
    detail = models.TextField('操作详情', blank=True, default='')
    ip_address = models.CharField('IP地址', max_length=50, blank=True, default='')
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        db_table = 'operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.action} - {self.target}'
```

- [ ] **Step 7: 各 app 的 admin.py 注册模型**

`backend/apps/classes/admin.py`:

```python
from django.contrib import admin
from .models import ClassInfo

@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'major', 'student_count', 'created_at']
```

`backend/apps/teachers/admin.py`:

```python
from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_no', 'name', 'gender', 'title', 'class_ref']
```

`backend/apps/students/admin.py`:

```python
from django.contrib import admin
from .models import Student, InfoChangeRequest

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_no', 'name', 'gender', 'class_ref', 'status']

@admin.register(InfoChangeRequest)
class InfoChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'field_name', 'status', 'created_at']
```

`backend/apps/courses/admin.py`:

```python
from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'credit', 'class_ref', 'teacher']
```

`backend/apps/scores/admin.py`:

```python
from django.contrib import admin
from .models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'score', 'semester']
```

`backend/apps/logs/admin.py`:

```python
from django.contrib import admin
from .models import OperationLog

@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'target', 'created_at']
```

- [ ] **Step 8: 数据库迁移**

```bash
cd E:/personPro/stuMan/backend
python manage.py makemigrations
python manage.py migrate
```

- [ ] **Step 9: 提交**

```bash
git add backend/apps/
git commit -m "feat: add all data models (student, teacher, class, course, score, log)"
```

---

## Phase 2: 后端 API

### Task 4: 认证 API

**Files:**
- Create: `backend/apps/users/views.py`
- Create: `backend/apps/users/urls.py`
- Modify: `backend/stuMan/urls.py`

- [ ] **Step 1: 编写认证视图**

替换 `backend/apps/users/views.py`:

```python
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer
from .models import User


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response({'detail': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'detail': '账号已被禁用'}, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': '已退出登录'})


class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        # 附加角色对应的详细信息
        if user.role == 'student' and hasattr(user, 'student_profile'):
            data['name'] = user.student_profile.name
            data['student_no'] = user.student_profile.student_no
        elif user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            data['name'] = user.teacher_profile.name
            data['teacher_no'] = user.teacher_profile.teacher_no
        return Response(data)


class ChangePasswordView(APIView):
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        login(request, user)
        return Response({'detail': '密码修改成功'})
```

- [ ] **Step 2: 编写用户路由**

创建 `backend/apps/users/urls.py`:

```python
from django.urls import path
from .views import LoginView, LogoutView, UserInfoView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('userinfo/', UserInfoView.as_view()),
    path('password/', ChangePasswordView.as_view()),
]
```

- [ ] **Step 3: 配置主路由**

替换 `backend/stuMan/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/teachers/', include('apps.teachers.urls')),
    path('api/classes/', include('apps.classes.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/scores/', include('apps.scores.urls')),
    path('api/logs/', include('apps.logs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- [ ] **Step 4: 测试启动**

```bash
cd E:/personPro/stuMan/backend
python manage.py runserver 0.0.0.0:8000
```

访问 `http://localhost:8000/admin/` 确认后台正常。

- [ ] **Step 5: 提交**

```bash
git add backend/apps/users/ backend/stuMan/urls.py
git commit -m "feat: add auth API (login, logout, userinfo, change password)"
```

---

### Task 5: 班级管理 API

**Files:**
- Create: `backend/apps/classes/serializers.py`
- Create: `backend/apps/classes/views.py`
- Create: `backend/apps/classes/urls.py`

- [ ] **Step 1: 序列化器**

创建 `backend/apps/classes/serializers.py`:

```python
from rest_framework import serializers
from .models import ClassInfo


class ClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInfo
        fields = '__all__'
        read_only_fields = ['id', 'student_count', 'created_at']
```

- [ ] **Step 2: 视图**

替换 `backend/apps/classes/views.py`:

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .models import ClassInfo
from .serializers import ClassInfoSerializer
from apps.users.permissions import IsAdmin


class ClassInfoViewSet(ModelViewSet):
    queryset = ClassInfo.objects.all()
    serializer_class = ClassInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'grade', 'major']
    permission_classes = [IsAdmin]
```

- [ ] **Step 3: 路由**

创建 `backend/apps/classes/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from .views import ClassInfoViewSet

router = DefaultRouter()
router.register('', ClassInfoViewSet, basename='class')
urlpatterns = router.urls
```

- [ ] **Step 4: 提交**

```bash
git add backend/apps/classes/
git commit -m "feat: add ClassInfo CRUD API"
```

---

### Task 6: 教师管理 API

**Files:**
- Create: `backend/apps/teachers/serializers.py`
- Create: `backend/apps/teachers/views.py`
- Create: `backend/apps/teachers/urls.py`

- [ ] **Step 1: 序列化器**

创建 `backend/apps/teachers/serializers.py`:

```python
from rest_framework import serializers
from .models import Teacher
from apps.users.models import User


class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'username', 'teacher_no', 'name', 'gender',
            'title', 'phone', 'email', 'class_ref', 'class_name',
        ]
        read_only_fields = ['id']


class TeacherCreateSerializer(serializers.Serializer):
    teacher_no = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=[('male', '男'), ('female', '女')])
    title = serializers.CharField(max_length=20, required=False, default='')
    phone = serializers.CharField(max_length=20, required=False, default='')
    email = serializers.EmailField(required=False, default='')
    class_ref = serializers.PrimaryKeyRelatedField(
        queryset=None, required=False, allow_null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.classes.models import ClassInfo
        self.fields['class_ref'].queryset = ClassInfo.objects.all()

    def validate_teacher_no(self, value):
        if Teacher.objects.filter(teacher_no=value).exists():
            raise serializers.ValidationError('工号已存在')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该工号对应的用户已存在')
        return value

    def create(self, validated_data):
        # 创建用户账号，默认密码为工号后6位
        username = validated_data['teacher_no']
        password = username[-6:]
        user = User.objects.create_user(
            username=username, password=password, role='teacher', is_active=True,
        )
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
```

- [ ] **Step 2: 视图**

替换 `backend/apps/teachers/views.py`:

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import Teacher
from .serializers import TeacherSerializer, TeacherCreateSerializer
from apps.users.permissions import IsAdmin


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.select_related('user', 'class_ref').all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'teacher_no']
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        return TeacherSerializer

    @action(detail=True, methods=['put'], url_path='toggle')
    def toggle_active(self, request, pk=None):
        teacher = self.get_object()
        teacher.user.is_active = not teacher.user.is_active
        teacher.user.save()
        return Response({'is_active': teacher.user.is_active})
```

- [ ] **Step 3: 路由**

创建 `backend/apps/teachers/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register('', TeacherViewSet, basename='teacher')
urlpatterns = router.urls
```

- [ ] **Step 4: 提交**

```bash
git add backend/apps/teachers/
git commit -m "feat: add Teacher CRUD API with auto user creation"
```

---

### Task 7: 学生管理 API

**Files:**
- Create: `backend/apps/students/serializers.py`
- Create: `backend/apps/students/views.py`
- Create: `backend/apps/students/urls.py`
- Create: `backend/apps/students/filters.py`

- [ ] **Step 1: 过滤器**

创建 `backend/apps/students/filters.py`:

```python
import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    class_ref = django_filters.NumberFilter(field_name='class_ref__id')
    name = django_filters.CharFilter(lookup_expr='icontains')
    student_no = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['class_ref', 'name', 'student_no', 'gender', 'status']
```

- [ ] **Step 2: 序列化器**

创建 `backend/apps/students/serializers.py`:

```python
from rest_framework import serializers
from .models import Student, InfoChangeRequest
from apps.users.models import User


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'username', 'student_no', 'name', 'gender', 'age',
            'class_ref', 'class_name', 'phone', 'email', 'address', 'avatar', 'status',
        ]
        read_only_fields = ['id', 'status']


class StudentCreateSerializer(serializers.Serializer):
    student_no = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=[('male', '男'), ('female', '女')])
    age = serializers.IntegerField(required=False, allow_null=True)
    class_ref = serializers.PrimaryKeyRelatedField(queryset=None, required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, default='')
    email = serializers.EmailField(required=False, default='')
    address = serializers.CharField(max_length=200, required=False, default='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.classes.models import ClassInfo
        self.fields['class_ref'].queryset = ClassInfo.objects.all()

    def validate_student_no(self, value):
        if Student.objects.filter(student_no=value).exists():
            raise serializers.ValidationError('学号已存在')
        return value

    def create(self, validated_data):
        username = validated_data['student_no']
        password = username[-6:]
        user = User.objects.create_user(
            username=username, password=password, role='student', is_active=True,
        )
        student = Student.objects.create(user=user, **validated_data)
        # 更新班级人数
        if student.class_ref:
            student.class_ref.student_count = student.class_ref.students.count()
            student.class_ref.save()
        return student


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'gender', 'age', 'class_ref', 'phone', 'email', 'address']


class InfoChangeRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = InfoChangeRequest
        fields = [
            'id', 'student', 'student_name', 'field_name', 'old_value',
            'new_value', 'status', 'reviewer', 'review_time', 'remark', 'created_at',
        ]
        read_only_fields = ['id', 'status', 'reviewer', 'review_time', 'created_at']
```

- [ ] **Step 3: 视图**

替换 `backend/apps/students/views.py`:

```python
import io
from datetime import datetime
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
import openpyxl

from .models import Student, InfoChangeRequest
from .serializers import (
    StudentSerializer, StudentCreateSerializer, StudentUpdateSerializer,
    InfoChangeRequestSerializer,
)
from .filters import StudentFilter
from apps.users.permissions import IsAdminOrTeacher, IsStudent, IsAdmin


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('user', 'class_ref').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ['name', 'student_no']
    ordering_fields = ['student_no', 'name']

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            return [IsAdminOrTeacher()]
        if self.action in ['update', 'partial_update', 'retrieve']:
            return [IsAdminOrTeacher()]
        return [IsAdminOrTeacher()]

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return StudentUpdateSerializer
        return StudentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # 教师只能看自己班级的学生
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            qs = qs.filter(class_ref=user.teacher_profile.class_ref)
        return qs

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        students = self.get_queryset()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = '学生信息'
        headers = ['学号', '姓名', '性别', '年龄', '班级', '电话', '邮箱', '地址']
        ws.append(headers)
        for s in students:
            ws.append([
                s.student_no, s.name, s.get_gender_display(), s.age,
                s.class_ref.name if s.class_ref else '', s.phone, s.email, s.address,
            ])
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename=students_{datetime.now():%Y%m%d}.xlsx'
        return response

    @action(detail=False, methods=['post'], url_path='import')
    def import_excel(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': '请上传文件'}, status=status.HTTP_400_BAD_REQUEST)
        wb = openpyxl.load_workbook(file)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        created = 0
        for row in rows:
            student_no, name, gender_str, age, class_name, phone, email, address = (
                row[0], row[1], row[2], row[3], row[4],
                row[5] or '', row[6] or '', row[7] or '',
            )
            if Student.objects.filter(student_no=str(student_no)).exists():
                continue
            gender = 'male' if gender_str == '男' else 'female'
            from apps.classes.models import ClassInfo
            class_ref = ClassInfo.objects.filter(name=class_name).first()
            username = str(student_no)
            password = username[-6:]
            user = User.objects.create_user(
                username=username, password=password, role='student', is_active=True,
            )
            Student.objects.create(
                user=user, student_no=str(student_no), name=str(name),
                gender=gender, age=int(age) if age else None,
                class_ref=class_ref, phone=str(phone), email=str(email), address=str(address),
            )
            created += 1
        return Response({'detail': f'成功导入 {created} 条'})


class InfoChangeRequestViewSet(ModelViewSet):
    queryset = InfoChangeRequest.objects.select_related('student', 'reviewer').all()
    serializer_class = InfoChangeRequestSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'student':
            return qs.filter(student__user=user)
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            return qs.filter(student__class_ref=user.teacher_profile.class_ref)
        return qs

    def perform_create(self, serializer):
        student = Student.objects.get(user=self.request.user)
        student.status = 'pending'
        student.save()
        serializer.save(student=student)

    @action(detail=True, methods=['put'], url_path='approve')
    def approve(self, request, pk=None):
        change = self.get_object()
        change.status = 'approved'
        change.reviewer = request.user
        change.review_time = datetime.now()
        change.save()
        # 更新学生信息
        student = change.student
        setattr(student, change.field_name, change.new_value)
        student.status = 'normal'
        student.save()
        return Response({'detail': '审核通过'})

    @action(detail=True, methods=['put'], url_path='reject')
    def reject(self, request, pk=None):
        change = self.get_object()
        change.status = 'rejected'
        change.reviewer = request.user
        change.review_time = datetime.now()
        change.remark = request.data.get('remark', '')
        change.save()
        student = change.student
        student.status = 'normal'
        student.save()
        return Response({'detail': '已驳回'})
```

- [ ] **Step 4: 路由**

创建 `backend/apps/students/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, InfoChangeRequestViewSet

router = DefaultRouter()
router.register('info-changes', InfoChangeRequestViewSet, basename='info-change')
router.register('', StudentViewSet, basename='student')
urlpatterns = router.urls
```

- [ ] **Step 5: 提交**

```bash
git add backend/apps/students/
git commit -m "feat: add Student CRUD API with import/export and approval flow"
```

---

### Task 8: 课程管理 API

**Files:**
- Create: `backend/apps/courses/serializers.py`
- Create: `backend/apps/courses/views.py`
- Create: `backend/apps/courses/urls.py`

- [ ] **Step 1: 序列化器**

创建 `backend/apps/courses/serializers.py`:

```python
from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True, default='')
    class_name = serializers.CharField(source='class_ref.name', read_only=True, default='')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'credit', 'class_ref', 'class_name',
            'teacher', 'teacher_name', 'description', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
```

- [ ] **Step 2: 视图**

替换 `backend/apps/courses/views.py`:

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer
from apps.users.permissions import IsAdminOrTeacher


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('class_ref', 'teacher').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['class_ref']
    search_fields = ['name']
    permission_classes = [IsAdminOrTeacher]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            qs = qs.filter(class_ref=user.teacher_profile.class_ref)
        return qs
```

- [ ] **Step 3: 路由**

创建 `backend/apps/courses/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register('', CourseViewSet, basename='course')
urlpatterns = router.urls
```

- [ ] **Step 4: 提交**

```bash
git add backend/apps/courses/
git commit -m "feat: add Course CRUD API"
```

---

### Task 9: 成绩管理 API

**Files:**
- Create: `backend/apps/scores/serializers.py`
- Create: `backend/apps/scores/views.py`
- Create: `backend/apps/scores/urls.py`

- [ ] **Step 1: 序列化器**

创建 `backend/apps/scores/serializers.py`:

```python
from rest_framework import serializers
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_no = serializers.CharField(source='student.student_no', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Score
        fields = [
            'id', 'student', 'student_name', 'student_no',
            'course', 'course_name', 'score', 'semester',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScoreBatchSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    semester = serializers.CharField(max_length=20)
    scores = serializers.ListField(
        child=serializers.DictField(), help_text='[{"student": id, "score": float}, ...]'
    )
```

- [ ] **Step 2: 视图**

替换 `backend/apps/scores/views.py`:

```python
import io
from datetime import datetime
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
import openpyxl

from .models import Score
from .serializers import ScoreSerializer, ScoreBatchSerializer
from apps.users.permissions import IsAdminOrTeacher, IsStudent


class ScoreViewSet(ModelViewSet):
    queryset = Score.objects.select_related('student', 'course').all()
    serializer_class = ScoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'student', 'semester']
    search_fields = ['student__name', 'student__student_no', 'course__name']
    ordering_fields = ['score', 'created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'student':
            return qs.filter(student__user=user)
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            return qs.filter(student__class_ref=user.teacher_profile.class_ref)
        return qs

    @action(detail=False, methods=['post'], url_path='batch')
    def batch_create(self, request):
        serializer = ScoreBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        from apps.courses.models import Course
        from apps.students.models import Student
        course = Course.objects.get(id=data['course'])
        created = 0
        for item in data['scores']:
            student = Student.objects.get(id=item['student'])
            obj, is_new = Score.objects.update_or_create(
                student=student, course=course, semester=data['semester'],
                defaults={'score': item['score']},
            )
            if is_new:
                created += 1
        return Response({'detail': f'录入 {created} 条成绩'})

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        course_id = request.query_params.get('course')
        qs = self.get_queryset()
        if course_id:
            qs = qs.filter(course_id=course_id)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = '成绩'
        headers = ['学号', '姓名', '课程', '成绩', '学期']
        ws.append(headers)
        for s in qs:
            ws.append([
                s.student.student_no, s.student.name,
                s.course.name, s.score, s.semester,
            ])
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename=scores_{datetime.now():%Y%m%d}.xlsx'
        return response
```

- [ ] **Step 3: 路由**

创建 `backend/apps/scores/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from .views import ScoreViewSet

router = DefaultRouter()
router.register('', ScoreViewSet, basename='score')
urlpatterns = router.urls
```

- [ ] **Step 4: 提交**

```bash
git add backend/apps/scores/
git commit -m "feat: add Score API with batch entry and Excel export"
```

---

### Task 10: 操作日志 API

**Files:**
- Create: `backend/apps/logs/serializers.py`
- Create: `backend/apps/logs/views.py`
- Create: `backend/apps/logs/urls.py`
- Create: `backend/apps/logs/middleware.py`

- [ ] **Step 1: 日志中间件**

创建 `backend/apps/logs/middleware.py`:

```python
import json
from .models import OperationLog

# 需要记录日志的路径关键字
LOG_PATHS = [
    '/api/students/', '/api/teachers/', '/api/classes/',
    '/api/courses/', '/api/scores/', '/api/info-changes/',
]

LOG_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']


class OperationLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method in LOG_METHODS
            and any(path in request.path for path in LOG_PATHS)
            and request.user.is_authenticated
        ):
            try:
                OperationLog.objects.create(
                    user=request.user,
                    action=request.method,
                    target=request.path,
                    detail=f'{request.method} {request.path}',
                    ip_address=self.get_client_ip(request),
                )
            except Exception:
                pass
        return response

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0]
        return request.META.get('REMOTE_ADDR', '')
```

在 `settings.py` 的 MIDDLEWARE 末尾添加：

```python
'apps.logs.middleware.OperationLogMiddleware',
```

- [ ] **Step 2: 序列化器**

创建 `backend/apps/logs/serializers.py`:

```python
from rest_framework import serializers
from .models import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, default='')

    class Meta:
        model = OperationLog
        fields = ['id', 'user', 'username', 'action', 'target', 'detail', 'ip_address', 'created_at']
```

- [ ] **Step 3: 视图**

替换 `backend/apps/logs/views.py`:

```python
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import OperationLog
from .serializers import OperationLogSerializer
from apps.users.permissions import IsAdmin


class OperationLogListView(ListAPIView):
    queryset = OperationLog.objects.select_related('user').all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['action']
    search_fields = ['user__username', 'target']
    ordering = ['-created_at']
```

- [ ] **Step 4: 路由**

创建 `backend/apps/logs/urls.py`:

```python
from django.urls import path
from .views import OperationLogListView

urlpatterns = [
    path('', OperationLogListView.as_view()),
]
```

- [ ] **Step 5: 提交**

```bash
git add backend/apps/logs/ backend/stuMan/settings.py
git commit -m "feat: add operation log middleware and API"
```

---

### Task 11: 数据统计 API

**Files:**
- Create: `backend/apps/users/stats_views.py`
- Modify: `backend/stuMan/urls.py`

- [ ] **Step 1: 统计视图**

创建 `backend/apps/users/stats_views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.classes.models import ClassInfo
from apps.courses.models import Course
from apps.scores.models import Score
from apps.users.permissions import IsAdminOrTeacher


class DashboardView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            return Response({
                'student_count': Student.objects.count(),
                'teacher_count': Teacher.objects.count(),
                'class_count': ClassInfo.objects.count(),
                'course_count': Course.objects.count(),
            })
        # 教师只看自己班级
        class_ref = user.teacher_profile.class_ref
        return Response({
            'student_count': Student.objects.filter(class_ref=class_ref).count(),
            'teacher_count': 1,
            'class_count': 1,
            'course_count': Course.objects.filter(class_ref=class_ref).count(),
        })


class ScoreDistributionView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        course_id = request.query_params.get('course')
        qs = Score.objects.all()
        if course_id:
            qs = qs.filter(course_id=course_id)
        if request.user.role == 'teacher':
            class_ref = request.user.teacher_profile.class_ref
            qs = qs.filter(student__class_ref=class_ref)
        levels = {'优秀': 0, '良好': 0, '中等': 0, '及格': 0, '不及格': 0}
        for s in qs:
            if s.score >= 90:
                levels['优秀'] += 1
            elif s.score >= 80:
                levels['良好'] += 1
            elif s.score >= 70:
                levels['中等'] += 1
            elif s.score >= 60:
                levels['及格'] += 1
            else:
                levels['不及格'] += 1
        return Response(levels)


class ClassStudentsView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        classes = ClassInfo.objects.all()
        data = [{'name': c.name, 'count': c.student_count} for c in classes]
        return Response(data)
```

- [ ] **Step 2: 注册路由**

修改 `backend/stuMan/urls.py`，在 urlpatterns 中添加：

```python
from apps.users.stats_views import DashboardView, ScoreDistributionView, ClassStudentsView

# 在 urlpatterns 中添加:
path('api/stats/dashboard/', DashboardView.as_view()),
path('api/stats/score-distribution/', ScoreDistributionView.as_view()),
path('api/stats/class-students/', ClassStudentsView.as_view()),
```

- [ ] **Step 3: 提交**

```bash
git add backend/apps/users/stats_views.py backend/stuMan/urls.py
git commit -m "feat: add statistics API (dashboard, score distribution, class students)"
```

---

## Phase 3: 前端

### Task 12: Vue 项目初始化

- [ ] **Step 1: 创建 Vue 项目**

```bash
cd E:/personPro/stuMan
npm create vite@latest frontend -- --template vue
cd frontend
npm install
npm install vue-router@4 pinia axios element-plus @element-plus/icons-vue echarts
```

- [ ] **Step 2: 配置 vite.config.js**

替换 `frontend/vite.config.js`:

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

- [ ] **Step 3: main.js**

替换 `frontend/src/main.js`:

```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
```

- [ ] **Step 4: App.vue**

替换 `frontend/src/App.vue`:

```vue
<template>
  <router-view />
</template>
```

- [ ] **Step 5: 提交**

```bash
cd E:/personPro/stuMan
git add frontend/
git commit -m "feat: initialize Vue 3 project with Element Plus, Pinia, Router"
```

---

### Task 13: Axios 封装和用户 Store

**Files:**
- Create: `frontend/src/api/index.js`
- Create: `frontend/src/store/user.js`
- Create: `frontend/src/utils/permission.js`

- [ ] **Step 1: Axios 实例**

创建 `frontend/src/api/index.js`:

```js
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        router.push('/login')
      } else if (error.response.status === 403) {
        ElMessage.error('无权限')
      } else {
        ElMessage.error(error.response.data?.detail || '请求失败')
      }
    }
    return Promise.reject(error)
  }
)

export default request
```

- [ ] **Step 2: 用户 Store**

创建 `frontend/src/store/user.js`:

```js
import { defineStore } from 'pinia'
import request from '../api'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    isLoggedIn: false,
  }),
  actions: {
    async login(username, password) {
      const data = await request.post('/auth/login/', { username, password })
      this.userInfo = data
      this.isLoggedIn = true
      return data
    },
    async logout() {
      await request.post('/auth/logout/')
      this.userInfo = null
      this.isLoggedIn = false
    },
    async fetchUserInfo() {
      const data = await request.get('/auth/userinfo/')
      this.userInfo = data
      this.isLoggedIn = true
      return data
    },
  },
})
```

- [ ] **Step 3: 权限菜单配置**

创建 `frontend/src/utils/permission.js`:

```js
export const menuConfig = {
  admin: [
    { path: '/dashboard', icon: 'DataAnalysis', title: '仪表盘' },
    { path: '/students', icon: 'User', title: '学生管理' },
    { path: '/teachers', icon: 'Avatar', title: '教师管理' },
    { path: '/classes', icon: 'School', title: '班级管理' },
    { path: '/courses', icon: 'Reading', title: '课程管理' },
    { path: '/scores', icon: 'Document', title: '成绩管理' },
    { path: '/info-changes', icon: 'Checked', title: '信息审核' },
    { path: '/logs', icon: 'List', title: '操作日志' },
  ],
  teacher: [
    { path: '/dashboard', icon: 'DataAnalysis', title: '仪表盘' },
    { path: '/students', icon: 'User', title: '学生管理' },
    { path: '/courses', icon: 'Reading', title: '课程管理' },
    { path: '/scores', icon: 'Document', title: '成绩管理' },
    { path: '/info-changes', icon: 'Checked', title: '信息审核' },
  ],
  student: [
    { path: '/scores', icon: 'Document', title: '我的成绩' },
    { path: '/my-applications', icon: 'Edit', title: '我的申请' },
    { path: '/profile', icon: 'User', title: '个人信息' },
  ],
}
```

- [ ] **Step 4: 提交**

```bash
git add frontend/src/api/ frontend/src/store/ frontend/src/utils/
git commit -m "feat: add Axios config, user store, and permission menu"
```

---

### Task 14: 路由和布局

**Files:**
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/views/Layout.vue`
- Create: `frontend/src/views/Login.vue`

- [ ] **Step 1: 路由配置**

创建 `frontend/src/router/index.js`:

```js
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  { path: '/login', component: () => import('../views/Login.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: '仪表盘' } },
      { path: 'students', component: () => import('../views/students/StudentList.vue'), meta: { title: '学生管理' } },
      { path: 'students/:id', component: () => import('../views/students/StudentDetail.vue'), meta: { title: '学生详情' } },
      { path: 'teachers', component: () => import('../views/teachers/TeacherList.vue'), meta: { title: '教师管理' } },
      { path: 'classes', component: () => import('../views/classes/ClassList.vue'), meta: { title: '班级管理' } },
      { path: 'courses', component: () => import('../views/courses/CourseList.vue'), meta: { title: '课程管理' } },
      { path: 'scores', component: () => import('../views/scores/ScoreList.vue'), meta: { title: '成绩管理' } },
      { path: 'scores/entry/:courseId', component: () => import('../views/scores/ScoreEntry.vue'), meta: { title: '成绩录入' } },
      { path: 'info-changes', component: () => import('../views/info-changes/InfoChangeList.vue'), meta: { title: '信息审核' } },
      { path: 'my-applications', component: () => import('../views/info-changes/MyApplications.vue'), meta: { title: '我的申请' } },
      { path: 'profile', component: () => import('../views/Profile.vue'), meta: { title: '个人信息' } },
      { path: 'change-password', component: () => import('../views/ChangePassword.vue'), meta: { title: '修改密码' } },
      { path: 'logs', component: () => import('../views/logs/LogList.vue'), meta: { title: '操作日志' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.public) return next()
  const store = useUserStore()
  if (!store.isLoggedIn) {
    try {
      await store.fetchUserInfo()
    } catch {
      return next('/login')
    }
  }
  next()
})

export default router
```

- [ ] **Step 2: Layout 布局**

创建 `frontend/src/views/Layout.vue`:

```vue
<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" style="background: #304156">
      <div style="height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; font-weight: bold">
        学生信息管理系统
      </div>
      <el-menu
        :default-active="$route.path"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        router
      >
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #eee">
        <span style="font-size: 16px">{{ $route.meta.title }}</span>
        <el-dropdown @command="handleCommand">
          <span style="cursor: pointer">
            {{ userStore.userInfo?.name || userStore.userInfo?.username }}
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              <el-dropdown-item command="password">修改密码</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { menuConfig } from '../utils/permission'

const router = useRouter()
const userStore = useUserStore()

const menus = computed(() => {
  const role = userStore.userInfo?.role
  return menuConfig[role] || []
})

const handleCommand = (cmd) => {
  if (cmd === 'profile') router.push('/profile')
  else if (cmd === 'password') router.push('/change-password')
  else if (cmd === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}
</script>
```

- [ ] **Step 3: 登录页**

创建 `frontend/src/views/Login.vue`:

```vue
<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
    <el-card style="width: 400px">
      <h2 style="text-align: center; margin-bottom: 30px">学生信息管理系统</h2>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="请输入账号" prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%" :loading="loading" native-type="submit">登 录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    router.push('/')
  } catch {
    ElMessage.error('登录失败')
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 4: 提交**

```bash
git add frontend/src/router/ frontend/src/views/Layout.vue frontend/src/views/Login.vue
git commit -m "feat: add router, layout, and login page"
```

---

### Task 15: 各管理页面

由于页面较多，这里给出关键页面的完整代码，其余页面结构类似。

- [ ] **Step 1: Dashboard.vue**

创建 `frontend/src/views/Dashboard.vue`:

```vue
<template>
  <div>
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6" v-for="item in cards" :key="item.label">
        <el-card shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 32px; color: #409eff; font-weight: bold">{{ item.value }}</div>
            <div style="color: #999; margin-top: 8px">{{ item.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>成绩等级分布</template>
          <div ref="scoreChart" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>班级学生人数</template>
          <div ref="classChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import request from '../api'

const cards = ref([])
const scoreChart = ref(null)
const classChart = ref(null)

onMounted(async () => {
  const data = await request.get('/stats/dashboard/')
  cards.value = [
    { label: '学生总数', value: data.student_count },
    { label: '教师总数', value: data.teacher_count },
    { label: '班级数量', value: data.class_count },
    { label: '课程数量', value: data.course_count },
  ]

  // 成绩分布饼图
  const scoreData = await request.get('/stats/score-distribution/')
  const pie = echarts.init(scoreChart.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: '60%',
      data: Object.entries(scoreData).map(([name, value]) => ({ name, value })),
    }],
  })

  // 班级人数柱状图
  const classData = await request.get('/stats/class-students/')
  const bar = echarts.init(classChart.value)
  bar.setOption({
    tooltip: {},
    xAxis: { type: 'category', data: classData.map(c => c.name) },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: classData.map(c => c.count) }],
  })
})
</script>
```

- [ ] **Step 2: StudentList.vue**

创建 `frontend/src/views/students/StudentList.vue`:

```vue
<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="姓名">
        <el-input v-model="query.name" placeholder="搜索姓名" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item label="学号">
        <el-input v-model="query.student_no" placeholder="搜索学号" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">搜索</el-button>
        <el-button type="success" @click="showAdd">新增学生</el-button>
        <el-button @click="handleExport">导出 Excel</el-button>
        <el-upload :show-file-list="false" :before-upload="handleImport" accept=".xlsx,.xls">
          <el-button>导入 Excel</el-button>
        </el-upload>
      </el-form-item>
    </el-form>

    <el-table :data="list" border stripe>
      <el-table-column prop="student_no" label="学号" width="120" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="gender" label="性别" width="60">
        <template #default="{ row }">{{ row.gender === 'male' ? '男' : '女' }}</template>
      </el-table-column>
      <el-table-column prop="class_name" label="班级" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'normal' ? 'success' : 'warning'">
            {{ row.status === 'normal' ? '正常' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 16px; justify-content: center"
      v-model:current-page="page"
      :page-size="10"
      :total="total"
      layout="prev, pager, next"
      @current-change="loadData"
    />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学生' : '新增学生'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="学号"><el-input v-model="form.student_no" :disabled="isEdit" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄"><el-input-number v-model="form.age" :min="1" :max="100" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="地址"><el-input v-model="form.address" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const page = ref(1)
const query = reactive({ name: '', student_no: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const classList = ref([])
const form = reactive({
  student_no: '', name: '', gender: 'male', age: null,
  class_ref: null, phone: '', email: '', address: '',
})

const loadData = async () => {
  const data = await request.get('/students/', { params: { page: page.value, ...query } })
  list.value = data.results
  total.value = data.count
}

const loadClasses = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { student_no: '', name: '', gender: 'male', age: null, class_ref: null, phone: '', email: '', address: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, gender: row.gender, age: row.age, class_ref: row.class_ref, phone: row.phone, email: row.email, address: row.address })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/students/${editId.value}/`, form)
    ElMessage.success('修改成功')
  } else {
    await request.post('/students/', form)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/students/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

const handleExport = () => {
  window.open('/api/students/export/', '_blank')
}

const handleImport = async (file) => {
  const fd = new FormData()
  fd.append('file', file)
  await request.post('/students/import/', fd)
  ElMessage.success('导入完成')
  loadData()
  return false
}

onMounted(() => { loadData(); loadClasses() })
</script>
```

- [ ] **Step 3: TeacherList.vue**

创建 `frontend/src/views/teachers/TeacherList.vue`（结构与 StudentList 类似）:

```vue
<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="姓名">
        <el-input v-model="query.name" placeholder="搜索姓名" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">搜索</el-button>
        <el-button type="success" @click="showAdd">新增教师</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="list" border stripe>
      <el-table-column prop="teacher_no" label="工号" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别">
        <template #default="{ row }">{{ row.gender === 'male' ? '男' : '女' }}</template>
      </el-table-column>
      <el-table-column prop="title" label="职称" />
      <el-table-column prop="class_name" label="所带班级" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="handleToggle(row)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑教师' : '新增教师'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="工号"><el-input v-model="form.teacher_no" :disabled="isEdit" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="职称"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级" clearable>
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const page = ref(1)
const query = reactive({ name: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const classList = ref([])
const form = reactive({ teacher_no: '', name: '', gender: 'male', title: '', class_ref: null, phone: '', email: '' })

const loadData = async () => {
  const data = await request.get('/teachers/', { params: { page: page.value, ...query } })
  list.value = data.results
  total.value = data.count
}

const loadClasses = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { teacher_no: '', name: '', gender: 'male', title: '', class_ref: null, phone: '', email: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, gender: row.gender, title: row.title, class_ref: row.class_ref, phone: row.phone, email: row.email })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/teachers/${editId.value}/`, form)
  } else {
    await request.post('/teachers/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleToggle = async (row) => {
  await request.put(`/teachers/${row.id}/toggle/`)
  ElMessage.success('操作成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/teachers/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(() => { loadData(); loadClasses() })
</script>
```

- [ ] **Step 4: ClassList.vue**

创建 `frontend/src/views/classes/ClassList.vue`:

```vue
<template>
  <div>
    <el-button type="success" style="margin-bottom: 16px" @click="showAdd">新增班级</el-button>
    <el-table :data="list" border stripe>
      <el-table-column prop="name" label="班级名称" />
      <el-table-column prop="grade" label="年级" />
      <el-table-column prop="major" label="专业" />
      <el-table-column prop="student_count" label="学生人数" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑班级' : '新增班级'" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="班级名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="年级"><el-input v-model="form.grade" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="form.major" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', grade: '', major: '' })

const loadData = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  list.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { name: '', grade: '', major: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, grade: row.grade, major: row.major })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/classes/${editId.value}/`, form)
  } else {
    await request.post('/classes/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/classes/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(loadData)
</script>
```

- [ ] **Step 5: CourseList.vue**

创建 `frontend/src/views/courses/CourseList.vue`:

```vue
<template>
  <div>
    <el-button type="success" style="margin-bottom: 16px" @click="showAdd">新增课程</el-button>
    <el-table :data="list" border stripe>
      <el-table-column prop="name" label="课程名称" />
      <el-table-column prop="credit" label="学分" width="80" />
      <el-table-column prop="class_name" label="班级" />
      <el-table-column prop="teacher_name" label="授课教师" />
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" type="success" @click="$router.push(`/scores/entry/${row.id}`)">录入成绩</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑课程' : '新增课程'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="课程名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="学分"><el-input-number v-model="form.credit" :min="0.5" :step="0.5" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="form.teacher" placeholder="选择教师" clearable>
            <el-option v-for="t in teacherList" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const classList = ref([])
const teacherList = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', credit: 1, class_ref: null, teacher: null, description: '' })

const loadData = async () => {
  const data = await request.get('/courses/')
  list.value = data.results
}

const loadOptions = async () => {
  const [c, t] = await Promise.all([
    request.get('/classes/', { params: { page_size: 100 } }),
    request.get('/teachers/', { params: { page_size: 100 } }),
  ])
  classList.value = c.results
  teacherList.value = t.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { name: '', credit: 1, class_ref: null, teacher: null, description: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, credit: row.credit, class_ref: row.class_ref, teacher: row.teacher, description: row.description })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/courses/${editId.value}/`, form)
  } else {
    await request.post('/courses/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/courses/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(() => { loadData(); loadOptions() })
</script>
```

- [ ] **Step 6: ScoreList.vue 和 ScoreEntry.vue**

创建 `frontend/src/views/scores/ScoreList.vue`:

```vue
<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="课程">
        <el-select v-model="query.course" placeholder="全部课程" clearable @change="loadData">
          <el-option v-for="c in courseList" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="学期">
        <el-input v-model="query.semester" placeholder="如 2025-2026-1" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">查询</el-button>
        <el-button @click="handleExport">导出 Excel</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="list" border stripe>
      <el-table-column prop="student_no" label="学号" />
      <el-table-column prop="student_name" label="姓名" />
      <el-table-column prop="course_name" label="课程" />
      <el-table-column prop="score" label="成绩" width="80" />
      <el-table-column prop="semester" label="学期" />
      <el-table-column label="操作" width="100" v-if="userStore.userInfo?.role !== 'student'">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { useUserStore } from '../../store/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const list = ref([])
const total = ref(0)
const page = ref(1)
const courseList = ref([])
const query = reactive({ course: null, semester: '' })

const loadData = async () => {
  const params = { page: page.value }
  if (query.course) params.course = query.course
  if (query.semester) params.semester = query.semester
  const data = await request.get('/scores/', { params })
  list.value = data.results
  total.value = data.count
}

const loadCourses = async () => {
  const data = await request.get('/courses/', { params: { page_size: 100 } })
  courseList.value = data.results
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/scores/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

const handleExport = () => {
  const params = new URLSearchParams()
  if (query.course) params.append('course', query.course)
  window.open(`/api/scores/export/?${params}`, '_blank')
}

onMounted(() => { loadData(); loadCourses() })
</script>
```

创建 `frontend/src/views/scores/ScoreEntry.vue`:

```vue
<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="学期">
        <el-input v-model="semester" placeholder="如 2025-2026-1" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadStudents">加载学生</el-button>
        <el-button type="success" @click="handleSubmit" :disabled="!scores.length">提交成绩</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="scores" border stripe>
      <el-table-column prop="student_no" label="学号" width="120" />
      <el-table-column prop="student_name" label="姓名" width="120" />
      <el-table-column label="成绩">
        <template #default="{ row }">
          <el-input-number v-model="row.score" :min="0" :max="100" :precision="1" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../../api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const courseId = route.params.courseId
const semester = ref('')
const scores = ref([])

const loadStudents = async () => {
  if (!semester.value) {
    ElMessage.warning('请填写学期')
    return
  }
  // 获取课程对应的班级学生
  const course = await request.get(`/courses/${courseId}/`)
  const data = await request.get('/students/', { params: { class_ref: course.class_ref, page_size: 200 } })
  scores.value = data.results.map(s => ({
    student: s.id,
    student_no: s.student_no,
    student_name: s.name,
    score: null,
  }))
}

const handleSubmit = async () => {
  const validScores = scores.value.filter(s => s.score !== null)
  if (!validScores.length) {
    ElMessage.warning('请填写成绩')
    return
  }
  await request.post('/scores/batch/', {
    course: parseInt(courseId),
    semester: semester.value,
    scores: validScores.map(s => ({ student: s.student, score: s.score })),
  })
  ElMessage.success('成绩录入成功')
  router.push('/scores')
}
</script>
```

- [ ] **Step 7: InfoChangeList.vue 和 MyApplications.vue**

创建 `frontend/src/views/info-changes/InfoChangeList.vue`:

```vue
<template>
  <div>
    <el-table :data="list" border stripe>
      <el-table-column prop="student_name" label="学生" />
      <el-table-column prop="field_name" label="修改字段" />
      <el-table-column prop="old_value" label="原值" />
      <el-table-column prop="new_value" label="新值" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="{ pending: 'warning', approved: 'success', rejected: 'danger' }[row.status]">
            {{ { pending: '待审核', approved: '已通过', rejected: '已驳回' }[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="180" />
      <el-table-column label="操作" width="200" v-if="userStore.userInfo?.role !== 'student'">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button size="small" type="success" @click="handleApprove(row)">通过</el-button>
            <el-button size="small" type="danger" @click="handleReject(row)">驳回</el-button>
          </template>
          <span v-else>{{ row.remark }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api'
import { useUserStore } from '../../store/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const list = ref([])
const total = ref(0)
const page = ref(1)

const loadData = async () => {
  const data = await request.get('/info-changes/', { params: { page: page.value } })
  list.value = data.results
  total.value = data.count
}

const handleApprove = (row) => {
  ElMessageBox.confirm('确认通过？').then(async () => {
    await request.put(`/info-changes/${row.id}/approve/`)
    ElMessage.success('已通过')
    loadData()
  })
}

const handleReject = (row) => {
  ElMessageBox.prompt('请输入驳回原因').then(async ({ value }) => {
    await request.put(`/info-changes/${row.id}/reject/`, { remark: value })
    ElMessage.success('已驳回')
    loadData()
  })
}

onMounted(loadData)
</script>
```

创建 `frontend/src/views/info-changes/MyApplications.vue`:

```vue
<template>
  <div>
    <h3>我的申请记录</h3>
    <el-table :data="list" border stripe>
      <el-table-column prop="field_name" label="修改字段" />
      <el-table-column prop="old_value" label="原值" />
      <el-table-column prop="new_value" label="新值" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="{ pending: 'warning', approved: 'success', rejected: 'danger' }[row.status]">
            {{ { pending: '待审核', approved: '已通过', rejected: '已驳回' }[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="审核备注" />
      <el-table-column prop="created_at" label="申请时间" width="180" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api'

const list = ref([])

onMounted(async () => {
  const data = await request.get('/info-changes/')
  list.value = data.results
})
</script>
```

- [ ] **Step 8: Profile.vue 和 ChangePassword.vue**

创建 `frontend/src/views/Profile.vue`:

```vue
<template>
  <div style="max-width: 600px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="账号">
        <el-input :value="userStore.userInfo?.username" disabled />
      </el-form-item>
      <el-form-item label="角色">
        <el-input :value="roleMap[userStore.userInfo?.role]" disabled />
      </el-form-item>
      <template v-if="profile">
        <el-form-item label="姓名"><el-input v-model="profile.name" :disabled="!canEdit" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="profile.gender" :disabled="!canEdit">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="profile.phone" :disabled="!canEdit" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="profile.email" :disabled="!canEdit" /></el-form-item>
        <el-form-item label="地址" v-if="userStore.userInfo?.role === 'student'">
          <el-input v-model="profile.address" :disabled="!canEdit" />
        </el-form-item>
      </template>
      <el-form-item>
        <el-button v-if="canEdit" type="primary" @click="handleSubmit">保存修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import request from '../api'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const profile = ref(null)
const roleMap = { admin: '管理员', teacher: '教师', student: '学生' }

const canEdit = computed(() => userStore.userInfo?.role !== 'admin')

onMounted(async () => {
  const role = userStore.userInfo?.role
  if (role === 'student') {
    profile.value = await request.get(`/students/${userStore.userInfo.id}/`)
  } else if (role === 'teacher') {
    profile.value = await request.get(`/teachers/${userStore.userInfo.id}/`)
  }
})

const handleSubmit = async () => {
  const role = userStore.userInfo?.role
  if (role === 'student') {
    // 学生修改需要审核
    await request.post('/info-changes/', {
      student: profile.value.id,
      field_name: 'info',
      old_value: '当前信息',
      new_value: '提交修改',
    })
    ElMessage.success('修改已提交，等待审核')
  } else if (role === 'teacher') {
    await request.put(`/teachers/${profile.value.id}/`, profile.value)
    ElMessage.success('修改成功')
  }
}
</script>
```

创建 `frontend/src/views/ChangePassword.vue`:

```vue
<template>
  <div style="max-width: 400px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="旧密码"><el-input v-model="form.old_password" type="password" show-password /></el-form-item>
      <el-form-item label="新密码"><el-input v-model="form.new_password" type="password" show-password /></el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">修改密码</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import request from '../api'
import { ElMessage } from 'element-plus'

const form = reactive({ old_password: '', new_password: '' })

const handleSubmit = async () => {
  await request.put('/auth/password/', form)
  ElMessage.success('密码修改成功')
}
</script>
```

- [ ] **Step 9: LogList.vue**

创建 `frontend/src/views/logs/LogList.vue`:

```vue
<template>
  <div>
    <el-table :data="list" border stripe>
      <el-table-column prop="username" label="操作人" width="120" />
      <el-table-column prop="action" label="操作类型" width="100" />
      <el-table-column prop="target" label="操作对象" />
      <el-table-column prop="detail" label="详情" />
      <el-table-column prop="ip_address" label="IP地址" width="140" />
      <el-table-column prop="created_at" label="操作时间" width="180" />
    </el-table>
    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api'

const list = ref([])
const total = ref(0)
const page = ref(1)

const loadData = async () => {
  const data = await request.get('/logs/', { params: { page: page.value } })
  list.value = data.results
  total.value = data.count
}

onMounted(loadData)
</script>
```

- [ ] **Step 10: 提交**

```bash
cd E:/personPro/stuMan
git add frontend/src/views/
git commit -m "feat: add all frontend pages (dashboard, students, teachers, classes, courses, scores, info-changes, logs, profile)"
```

---

## Phase 4: 收尾

### Task 16: 创建超级管理员并验证

- [ ] **Step 1: 创建超级管理员**

```bash
cd E:/personPro/stuMan/backend
python manage.py createsuperuser
# 用户名: admin, 密码: admin123, 角色手动在数据库设为 admin
```

在 Django shell 中设置角色：

```bash
python manage.py shell
>>> from apps.users.models import User
>>> u = User.objects.get(username='admin')
>>> u.role = 'admin'
>>> u.save()
```

- [ ] **Step 2: 启动服务验证**

```bash
# 终端1: 后端
cd E:/personPro/stuMan/backend
python manage.py runserver

# 终端2: 前端
cd E:/personPro/stuMan/frontend
npm run dev
```

访问 `http://localhost:5173` 验证登录功能。

- [ ] **Step 3: 最终提交**

```bash
cd E:/personPro/stuMan
git add .
git commit -m "feat: complete student management system v1.0"
```
