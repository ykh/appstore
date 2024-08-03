from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views.users_view import UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
