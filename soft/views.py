from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import View,TemplateView,ListView
from soft.models import Soft
from soft.forms import SoftForm
from users.models import CustomUser
import json
# Create your views here.

class SoftList(View):

    template_name = 'soft/soft_list.html'
    def get(self,request):

        soft_list = Soft.objects.all()
        context = {
            'title':['软件管理'],
            'soft_list':soft_list
        }

        return render(request,self.template_name,context)

class SoftEdit(View):
    template_name = 'soft/soft_edit.html'

    def get(self,request,**kwargs):
        uid = kwargs.get('uid',None)
        if uid:
            form = SoftForm(instance=Soft.objects.get(uuid=uid))
        else:
            form = SoftForm()

        context ={
            'title':['软件管理','添加软件信息'],
            'form':form
        }
        print(form)
        return render(request,self.template_name,context)

    def post(self,request,**kwargs):
        uid = kwargs.get('uid',None)
        if uid:
            form = SoftForm(request.POST,request.FILES,instance=Soft.objects.get(uuid=uid))
        else:
            form = SoftForm(request.POST,request.FILES)

        if form.is_valid():
            email = request.session.get('email')
            userObj = CustomUser.objects.get(email=email)
            if not uid:
                softObj = Soft()
                softObj.name = form.cleaned_data['name']
                softObj.soft_icon = form.cleaned_data['soft_icon']
                print(form.cleaned_data['soft_icon'])
                softObj.describe = form.cleaned_data['describe']
                softObj.version = form.cleaned_data['version']
                softObj.create_by = userObj
                softObj.save()
            else:
                server = form.save()

            return redirect('soft_list')
        else:
            print(form)
            return redirect('soft_list')


# def soft_add(request):
#     form = SoftForm
#     context ={
#             'title':['软件管理','添加软件信息'],
#             'form':form
#     }
#     if request.method == "POST":
#         form = SoftForm(request.POST,request.FILES)
#         if form.is_valid():
#             email = request.session.get('email')
#             userObj = CustomUser.objects.get(email=email)
#             softObj = Soft()
#             softObj.name = form.cleaned_data['name']
#             softObj.soft_icon = form.cleaned_data['soft_icon']
#             softObj.describe = form.cleaned_data['describe']
#             softObj.version = form.cleaned_data['version']
#             softObj.create_by = userObj
#             softObj.save()
#             return redirect('soft_list')
#     return render(request,'soft/soft_edit.html',context)


def soft_del(request):
    '''
    删除主机
    :param request:
    :param sid:
    :return:
    '''
    if request.method == "DELETE":
        uid = request.GET.get('uid')
        softObj = Soft.objects.filter(uuid__in=uid.split(','))
        try:
            softObj.delete()
            res = {"status":"ok"}
        except Exception as e:
            res = {"status":"error","data":str(e)}
        print(res)
        return HttpResponse(json.dumps(res,ensure_ascii=False))