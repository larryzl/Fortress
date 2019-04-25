from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
import json
import collections
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from assets.forms import ServerEditForm,ServerForm,IdcForm,ProjectForm,LabelForm
from assets.models import Server,IDC,Project,Label,ServerLog
from accounts.models import CustomUser
from django.urls import reverse_lazy
from accounts.auth_api import has_auth,get_node_list,get_user_id
from django.views.generic import View,TemplateView,ListView,DeleteView,UpdateView
from soft.models import Soft,ServerSoft


# Create your views here.

def server_log(*args,**kwargs):
    rows = kwargs.get('rows')
    ServerLog.objects.create(**rows)


class AssetsView(TemplateView):
    title = ['主机管理']
    template_name = 'assets/server_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': self.title
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetDeleteView(DeleteView):
    model = Server
    success_url = reverse_lazy('server_list')


class IDCView(TemplateView):
    title = [
        'IDC管理',
    ]
    template_name = 'assets/idc_list.html'

    def get_context_data(self, **kwargs):

        context = {
            'idcs' : IDC.objects.all().order_by('name'),
            'title': self.title
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class ServerView(View):
    title = [
        '主机管理','查看主机详情'
    ]
    #form = ServerFrom()

    template_name = 'assets/server_view.html'
    def get(self,request,uid,*args,**kwargs):
        try:
            server_info = Server.objects.get(uuid=uid)
            server_logs = ServerLog.objects.filter(host=server_info).order_by('-create_time')
            logs_list = collections.OrderedDict()
            for log in server_logs:
                date_field = log.create_time.date()
                logs_list.setdefault(date_field,[])
                logs_list[date_field].append([log.create_by,log.describe,log.detail,log.create_time.time()])
        except:
            err = "主机未找到"
            return render(request,self.template_name,{'err':err})

        context = {
            'title':self.title,
            'server_info':server_info,
            'logs_list':logs_list,
            'server_logs':server_logs,
            'soft_list': server_info.soft_set
        }
        return render(request,self.template_name,context)

class ServerEdit(View):
    title = [
        '主机管理',
        ''
    ]
    template_name = 'assets/server_edit.html'
    def get(self,request,*args,**kwargs):
        if 'uid' in kwargs.keys():
            uid = kwargs['uid']
            self.title[1]='修改资产信息'
            try:
                form = ServerEditForm(instance=Server.objects.get(uuid=uid))
            except:
                msg = "服务器未找到"
                return render(request,self.template_name,{'msg':msg})
        else:
            self.title[1]='创建资产信息'
            form = ServerEditForm()
        context = {
            'title': self.title,
            'form':form
        }
        return render(request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        uid = kwargs.get('uid',None)

        if uid:
            form = ServerEditForm(request.POST, instance=Server.objects.get(uuid=uid))
            describe = '修改主机信息:'
        else:
            form = ServerEditForm(request.POST)
            describe = '创建主机'
        if form.is_valid():
            email = request.session.get('email')
            # 获取登录用户
            userObj = CustomUser.objects.get(email=email)

            if not uid:
                server = form.save(commit=False)
                server.create_by = userObj
                server.save()
                form.save()
            else:
                form.save()

            hostObj = Server.objects.get(name=form.cleaned_data['name'])
            uid = hostObj.uuid
            # 保存日志
            try:

                changed_list = []
                name_dict = {'ssh_port':'SSH端口','ip':'内网IP','project':'项目组','label':'标签','is_active':'激活','idc_name':'IDC','ssh_user':'SSH用户','ip2':'公网IP','comment':'备注'}
                if form.has_changed()!=0:
                    for d in form.changed_data:
                        changed_list.append(name_dict[d])
                    rows = {
                        'describe':describe,
                        'create_by':userObj,
                        'host':hostObj,
                        'detail':",".join(changed_list)
                    }
                    server_log(rows=rows)
            except:
                rows = {
                  'describe':describe,'create_by':userObj,'host':hostObj,'detail':'主机创建成功'
                }
                server_log(rows=rows)


            return redirect('server_view',uid=uid)

class ServerSoftEdit(View):

    template_name="assets/server_soft.html"
    def get(self,request,**kwargs):
        uid = kwargs.pop('uid')
        if not uid:
            return redirect('server_list')
        serverObj = Server.objects.get(uuid=uid)
        server_soft = ServerSoft.objects.filter(server=serverObj)

        context = {
            'title':['主机管理','修改主机应用'],
            'is_install':Soft.objects.filter(server__name=serverObj),
            'all_softs':Soft.objects.all(),
            'uid':uid

        }
        return render(request,self.template_name,context)

    def post(self,request,**kwargs):
        # print(request.POST)
        try:

            soft_uid = request.POST.get('soft_uid')
            server_uid = kwargs.pop('uid')
            status = int(request.POST.get('status'))
            print(soft_uid,server_uid,status)
            if status == 1:
                softObj = Soft.objects.get(uuid=soft_uid).server.add(Server.objects.get(uuid=server_uid))
            elif status == 4:
                softObj = Soft.objects.get(uuid=soft_uid).server.remove(Server.objects.get(uuid=server_uid))
            else:
                print('not match')

            server_soft = ServerSoft()
            try:
                server_soft.objects.get(server_id=server_uid,soft_id=soft_uid)
                server_soft.status = status
                server_soft.save()
            except:
                server_soft.server = Server.objects.get(uuid=server_uid)
                server_soft.soft = Soft.objects.get(uuid=soft_uid)
                server_soft.status = int(status)
                server_soft.save()

            data = {'status':'true'}
        except Exception as e:
            data = {'status':'false'}
        print(data)
        return HttpResponse(json.dumps(data, ensure_ascii=False))



# def server_del(request):
#     '''
#     删除主机
#     :param request:
#     :param sid:
#     :return:
#     '''
#     if request.method == "DELETE":
#         sid = request.GET.get('uid')
#         server_obj = Server.objects.filter(uuid__in=sid.split(','))
#         print(sid.split(','))
#         try:
#             server_obj.delete()
#             res = {"status":"ok"}
#         except Exception as e:
#             res = {"status":"error","data":str(e)}
#         print(res)
#         return HttpResponse(json.dumps(res,ensure_ascii=False))

# def server_add_batch(request):
#     header_title = [
#         "主机管理","批量添加添加主机"
#     ]
#     title = header_title[-1]
#
#     idcs = IDC.objects.all()
#     os_list = server_os
#     if request.method == 'POST':
#         idc = request.POST.get('idc')
#         name_tag = request.POST.get('name')
#         ip_list = request.POST.getlist('ip')
#         os = request.POST.get('os')
#         for ip in ip_list:
#             name = name_tag+ip.split('.')[-1]
#             idc_name = IDC.objects.get(pk=idc)
#             # try:
#             Server.objects.create(name=name,ip=ip,idc_name=idc_name,system=os,ssh_port=22,ssh_user='root')
#             # except:
#             #     print(name,idc_name)
#         return redirect('server_list')
#
#     return render(request, 'assets/server_add_batch.html',locals())


def idc_del(request):
    if request.method == "DELETE":
        sid = request.GET.get('id')
        print(sid)
        if "," in sid:
            idc_obj = IDC.objects.filter(uuid__in=sid.split(','))
        else:
            idc_obj = IDC.objects.filter(uuid=sid)

        try:
            idc_obj.delete()
            res = {"status":"ok"}
        except:
            res = {"status":"error"}

        return HttpResponse(json.dumps(res,ensure_ascii=False))

    print('uuid IN (' + id + ')' )
    IDC.objects.extra(where=[ 'uuid IN (\'' + id + '\')' ]).delete()
    return HttpResponse('ok')
    # return render(request,'assets/server_list.html',locals())

class IdcEdit(View):
    '''
    IDC 编辑
    '''
    title = ['IDC管理','修改IDC信息']
    server_all_obj = Server.objects.all()
    template_name = 'assets/idc_edit.html'

    def get(self,request,**kwargs):
        uid = kwargs.pop('uid',None)
        if uid:
            form = IdcForm(instance=IDC.objects.get(uuid=uid))
            host_select = self.server_all_obj.filter(idc_name=IDC.objects.get(uuid=uid))
        else:
            self.title[1] = '添加IDC信息'
            form = IdcForm()
            host_select = []

        host_no_select = [server for server in self.server_all_obj if server not in host_select]

        context = {
            'title': self.title,
            'host_select': host_select,
            'host_no_select': host_no_select,
            'form': form,
            'uid': uid
        }
        return render(request,self.template_name,context)

    def post(self,request,**kwargs):
        uid = kwargs.pop('uid',None)
        if uid:
            form = IdcForm(request.POST,instance=IDC.objects.get(uuid=uid))
        else:
            form = IdcForm(request.POST)

        if form.is_valid():
            form.save()
            host_select = request.POST.getlist('hostSelect')
            print(host_select)
            if uid:
                idcObj = IDC.objects.get(uuid=uid)
                Server.objects.filter(uuid__in=host_select).update(idc_name=idcObj)

        return redirect('idc_list')



class ProjectList(View):
    template_name = 'assets/project_list.html'
    title = [
        '业务组管理',
    ]
    def get(self,request,*args,**kwargs):

        project_list = Project.objects.all()
        context = {
            'projects':project_list,
            'title':self.title

        }
        return render(request,self.template_name,context)

class ProjectAdd(View):

    header_title = [
        '业务组管理',
        '添加业务组'
    ]
    template_name = 'assets/project_add.html'
    form = ProjectForm()

    def get(self,request):

        context = {
            'title':self.header_title[0],
            'header':self.header_title[1],
            'form':self.form
        }
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')

class ProjectEdit(View):
    title = [
        '业务组管理','修改业务组'
    ]
    form = ProjectForm()
    model = Project
    template_name = 'assets/project_edit.html'
    server_all_obj = Server.objects.all()

    def get(self,request, *args, **kwargs):
        uid = kwargs.get('uid',None)
        if uid:
            form = ProjectForm(instance=Project.objects.get(uuid=uid))
            host_select = self.server_all_obj.filter(project=Project.objects.get(uuid=uid))
        else:
            self.title[1] = '添加业务组'
            form = ProjectForm()
            host_select = []

        host_no_select = [server for server in self.server_all_obj if server not in host_select]

        context = {
            'title': self.title,
            'host_select': host_select,
            'host_no_select': host_no_select,
            'form': form,
            'uid':uid
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        uid = kwargs.get('uid',None)
        if uid:
            project_obj = Project.objects.get(uuid=uid)
            form = ProjectForm(request.POST,instance=project_obj)
        else:
            form = ProjectForm(request.POST)

        if form.is_valid():
            if uid:
                assets_selected = request.POST.getlist('hostSelect')
                assets_no_selected = request.POST.getlist('hostNoSelect')
                for asset in assets_selected:
                    project_obj.server_set.add(Server.objects.get(uuid=asset))
                for asset in assets_no_selected:
                    project_obj.server_set.remove(Server.objects.get(uuid=asset))
            form.save()
        else:
            print(form)

        return redirect('project_list')


class LabelList(View):

    title = ["标签管理"]
    model = Label
    label_all = Label.objects.all()

    def get(self, request):
        context = {
            'title': self.title,
            'labels': self.label_all
        }
        return render(request, 'assets/label_list.html', context)


class LabelEdit(View):
    title = ['标签管理', '编辑标签']
    template_name = 'assets/lable_edit.html'
    server_all_obj = Server.objects.all()

    def get(self,request,**kwargs):
        uid = kwargs.get('uid', None)
        if uid:
            host_select = self.server_all_obj.filter(label=Label.objects.get(uuid=uid))
            form = LabelForm(instance=Label.objects.get(uuid=uid))
        else:
            form = LabelForm()
            host_select = []

        host_no_select = [server for server in self.server_all_obj if server not in host_select]
        context = {
            'title':self.title,
            'form':form,
            'uid':uid,
            'host_select': host_select,
            'host_no_select': host_no_select
        }
        return render(request,self.template_name,context)

    def post(self, request, **kwargs):
        uid = kwargs.get('uid', None)
        if uid:
            label_obj = Label.objects.get(uuid=uid)
            form = LabelForm(request.POST,instance=label_obj)
        else:
            form = LabelForm(request.POST)

        if form.is_valid():
            if uid:
                assets_selected = request.POST.getlist('hostSelect')
                assets_no_selected = request.POST.getlist('hostNoSelect')
                for asset in assets_selected:
                    label_obj.server_set.add(Server.objects.get(uuid=asset))
                for asset in assets_no_selected:
                    label_obj.server_set.remove(Server.objects.get(uuid=asset))
            form.save()
        else:
            print(form)

        return redirect('label_list')
