from django.urls import path
from django.contrib.auth import views as auth_views
from . import views




app_name = "common"

urlpatterns = [
    path("", views.HomeView.as_view(), name="main"),
    path('login/', views.CustomLoginView.as_view(template_name="account/login.html"), name="login"),
    #path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup")
]

# from .views import (
#     login_view,
#     logout_view,
#     signup_view,
# )

# app_name = 'account'
# urlpatterns = [
#     path('auth/', login_view, name='login'),
#     path('auth/expiration/', logout_view, name='logout'),
#     path('auth/new/', signup_view, name='signup'),
# ]
