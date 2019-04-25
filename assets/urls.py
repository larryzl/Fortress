from django.urls import path,re_path

from assets import views


urlpatterns = [
    # server url
    re_path('^server/$', views.AssetsView.as_view(),name='server_list'),
    re_path('^server/add/$',views.ServerEdit.as_view(),name='server_add'),
    re_path('^server/view/(?P<uid>[\w|-]+)/$',views.ServerView.as_view(),name='server_view'),
    re_path('^server/edit/(?P<uid>[\w|\-]+)/$',views.ServerEdit.as_view(),name='server_edit'),
    re_path('^server/edit/soft/(?P<uid>[\w|\-]+)/$',views.ServerSoftEdit.as_view(),name='server_soft'),
    # re_path('^server/change/status/',views.server_change_status,name='server_change_status'),
    re_path('^server/delete/(?P<uid>[\w|\-]+)/$',views.AssetDeleteView.as_view(),name='server_del'),
    # re_path(r'^server/add/batch',views.server_add_batch,name='server_add_batch'),
    #
    # idc url
    re_path(r'^idc/$',views.IDCView.as_view(),name='idc_list'),
    re_path(r'^idc/add$',views.IdcEdit.as_view(),name='idc_add'),
    re_path(r'^idc/del/',views.idc_del,name='idc_del'),
    re_path(r'^idc/edit/(?P<uid>[\w|\-]+)/$',views.IdcEdit.as_view(),name='idc_edit'),
    # project url
    re_path(r'^project/$',views.ProjectList.as_view(),name='project_list'),
    re_path(r'^project/add',views.ProjectEdit.as_view(),name='project_add'),
    re_path(r'^project/add',views.ProjectEdit.as_view(),name='project_del'),
    re_path(r'^project/edit/(?P<uid>[\w|\-]+)/$',views.ProjectEdit.as_view(),name='project_edit'),
    # label url
    re_path(r'^label/$',views.LabelList.as_view(),name='label_list'),
    re_path(r'^label/edit/(?P<uid>[\w|\-]+)/$',views.LabelEdit.as_view(),name='label_edit'),
    re_path(r'^label/add',views.LabelEdit.as_view(),name='label_add'),
    # re_path(r'^lable/edit/(?P<id>[\w|\-]+)/$',views.lable_edit,name='lable_edit'),

]

