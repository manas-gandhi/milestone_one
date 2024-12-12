from django.urls import path, include
from users.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path("user/", include("users.urls")),
    path("wallet/", include("wallets.urls")),
    path("transaction/", include("transactions.urls"))
]