""""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from email_parser import views
from email_parser.views import IndexView, dmarcListView, dmarc_checkView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('dmarc/', dmarcListView.as_view(), name='dmarc-list'),
    path('check/', dmarc_checkView.as_view(),name='dmarc_check'),
    path('emails/', views.email, name='email'),
    path('thanks/', views.thanks, name='thanks'),
]
