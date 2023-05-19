from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user import views


router = SimpleRouter()
router.register(r'auth',
                views.RegistrationModelViewSet,
                basename='auth')


urlpatterns = [
    path('', include(router.urls))
]
