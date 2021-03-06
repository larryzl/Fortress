"""Fortress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include,re_path
from .views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',index,name='index'),
    # re_path(r'^error_page.html',error_auth,name='error_auth'),
    # re_path(r'^test$',test_html),
    re_path(r'^assets/',include('assets.urls')),
    re_path(r'^users/',include('accounts.urls')),
    # re_path(r'^files/',include('files.urls')),
    # re_path(r'^jobs/',include('ansible_api.urls')),
    re_path(r'^ajax/',include('ajax.urls')),
    re_path(r'^auth/',include('authorize.urls')),
    re_path(r'^soft/',include('soft.urls')),
    re_path(r'^img/',include('mytest.urls'))
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'page_not_found'