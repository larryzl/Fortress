from django.urls import path,re_path

from soft import views


urlpatterns = [
    re_path('^$', views.SoftList.as_view(),name='soft_list'),
    re_path('^add$', views.SoftEdit.as_view(),name='soft_add'),
    re_path('^edit/(?P<uid>[\w|\-]+)/$', views.SoftEdit.as_view(),name='soft_edit'),
    re_path('^del/', views.soft_del,name='soft_del'),
]

