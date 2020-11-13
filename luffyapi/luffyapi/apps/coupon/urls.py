from django.urls import path,re_path
from . import views
urlpatterns = [
    path(r"",views.UserCouponListAPIView.as_view()),
]