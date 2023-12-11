from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='login'),
    path('signup/', views.RegisterNewUser.as_view(), name='signup'),
    path('account-verify/<slug:token>', views.account_verify, name='account-verify')
]
