from django.urls import path, include
from users.urls import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path("user/", include("users.urls")),
    path("transaction/", include("transactions.urls"))
]