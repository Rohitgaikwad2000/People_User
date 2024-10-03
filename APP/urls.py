from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("encrypt/", views.encrypt_message, name="encrypt_message"),
    path("decrypt-message/", views.decrypt_message, name="decrypt_message"),
    path("add-person/", views.add_person, name="add_person"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
