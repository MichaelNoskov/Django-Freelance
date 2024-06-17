"""URL configuration for django_sirius project."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from freelance import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet)
router.register('statuses', views.StatusViewSet)
router.register('positions', views.PositionViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = ()

urlpatterns = [
    path('', include('freelance.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
]
