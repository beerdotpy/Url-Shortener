"""urlShortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/create', views.register, name="register"),
    url(r'^user/login', views.login, name="login"),
    url(r'^url/short', views.shortenURL, name="shortenURL"),
    url(r'^url/delete', views.deleteURL, name="deleteURL"),
    url(r'^url/modify', views.modifyURL, name="modifyURL"),
    url(r'^(?P<shortURL>[-A-Za-z0-9_]+)/$', views.redirect, name='redirect'),
]

admin.site.site_header = 'URL Shortener Adminstration'