from django.conf.urls import url, include
from users.views import register, landing

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="registration"),
    url(r"^", landing, name="landing")
]
