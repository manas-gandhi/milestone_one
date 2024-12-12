from django.urls import path, include
from users.views import LoginView
from transactions.urls import transactions_urlpatterns, categories_urlpatterns

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path("user/", include("users.urls")),
    path("wallet/", include("wallets.urls")),
    path("transaction/", include(transactions_urlpatterns)),
    path("category/", include(categories_urlpatterns))
]