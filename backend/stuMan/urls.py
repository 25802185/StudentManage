from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.stats_views import DashboardView, ScoreDistributionView, ClassStudentsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/teachers/', include('apps.teachers.urls')),
    path('api/classes/', include('apps.classes.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/scores/', include('apps.scores.urls')),
    path('api/logs/', include('apps.logs.urls')),
    path('api/stats/dashboard/', DashboardView.as_view()),
    path('api/stats/score-distribution/', ScoreDistributionView.as_view()),
    path('api/stats/class-students/', ClassStudentsView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
