from mytest.views import save_profile,index
from django.urls import re_path
urlpatterns = [
    re_path('save_profile/', save_profile,name='save_profile'), # 新增
    re_path('index/', index,name='index')
]