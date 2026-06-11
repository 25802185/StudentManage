from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SemesterViewSet

router = DefaultRouter()
router.register('semesters', SemesterViewSet, basename='semester')
router.register('', CourseViewSet, basename='course')
urlpatterns = router.urls
