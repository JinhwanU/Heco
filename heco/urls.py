"""
URL configuration for heco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import BaseView, IndexView
from django.urls import path
from django.conf.urls import include
from heco import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path("", include("common.urls")),
    path('board/', include('board.urls')),
    path('chatbot/', include('gptChatBot.urls')),
    path('search/', include('search.urls')),
]

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path('base/', BaseView.as_view(), name='base'),
#     path('index/', IndexView.as_view(), name='index'),
#     path('board/', include('board.urls')),
#     path('account/', include('account.urls')),
# ]
