from django.urls import path
from .views import *

app_name = "bankid_sign"

urlpatterns = [
    path("", auth_root, name = "auth-root"),
    path("otherDevice/", auth_root_pc, name = "auth-root-pc"),
    path("mobile/", auth_root_mobile, name = "auth-root-mobile"),
    path("user/", auth_home, name = "auth-home"),
    path("failed/", auth_failed, name = "auth-failed"),
    path("logout/", auth_logout, name = "auth-logout"),
    path("status/<str:order_ref>/", collect_status, name = "collect-status"),
]