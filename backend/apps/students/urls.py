from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, InfoChangeRequestViewSet

router = DefaultRouter()
router.register('info-changes', InfoChangeRequestViewSet, basename='info-change')
router.register('', StudentViewSet, basename='student')
urlpatterns = router.urls
