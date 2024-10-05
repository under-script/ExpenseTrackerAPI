from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')
urlpatterns = router.urls
