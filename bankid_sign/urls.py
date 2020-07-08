from django.urls import path
from .views import *

app_name = "bankid_sign"

urlpatterns = [
    path("", auth_root, name = "auth-root"),
    path("logout/", auth_logout, name = "auth-logout"),
    path("status/<str:order_ref>/", collect_status, name = "collect-status"),
]