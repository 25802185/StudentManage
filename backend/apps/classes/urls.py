from rest_framework.routers import DefaultRouter
from .views import ClassInfoViewSet

router = DefaultRouter()
router.register('', ClassInfoViewSet, basename='class')
urlpatterns = router.urls
