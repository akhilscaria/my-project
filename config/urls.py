from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('customers/', include('customers.urls')),
]
