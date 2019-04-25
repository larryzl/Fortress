from assets.models import Server,Label,Project,IDC,ServerLog
from django import forms
from django.forms import widgets
from django.forms import fields

from django.utils.translation import gettext_lazy as _

def server_log(*args,**kwargs):
    try:
        rows = kwargs.get('rows')
        ServerLog.objects.create(**rows)
    except Exception as e:
        print(e)

class ServerForm(forms.ModelForm):
    ssh_port = forms.CharField(
        label="SSH端口",
        initial="22"
    )
    ssh_user = forms.CharField(
        label="SSH用户名",
        initial="root"
    )

    class Meta:
        model = Server
        fields = ('name','ip','project','label','is_active','system','idc_name','ssh_user','ssh_port','ansible_group')

class ServerEditForm(forms.ModelForm):

    # def __init__(self,*args,**kwargs):
    #     self.create_by = kwargs.pop('create_by')
    #     super(ServerEditForm,self).__init__(*args,**kwargs)

    name = fields.CharField(
        label="资产名称",
        error_messages={'required':'资产名称不能为空'},
        widget=widgets.Input(attrs={'class':"form-control"})
    )
    ip = fields.GenericIPAddressField(
        label="IP地址",
        error_messages={'required':'IP地址不能为空'},
        widget=widgets.Input(attrs={
            'class': 'form-control',
            'data-inputmask': "'alias': 'ip'",
            'data-mask': ''
        })
    )
    ssh_port = fields.IntegerField(
        label="SSH 端口",
        widget=widgets.Input(attrs={'class':'form-control'})
    )
    ip2 = fields.GenericIPAddressField(
        label="公网IP地址",
        required=False,
        widget=widgets.Input(attrs={
            'class': 'form-control',
            'data-inputmask': "'alias': 'ip'",
            'data-mask': ''
        })
    )

    class Meta:
        model = Server
        # exclude = ('create_by')
        fields = ['name','ip','project','label','is_active','idc_name','ssh_user','ssh_port','ip2','comment']
        widgets = {
            'project': forms.SelectMultiple(attrs={
                'class':'form-control select2','data-placeholder':'业务组'
            }),
            'label': forms.SelectMultiple(attrs={
                'class': 'form-control select2', 'data-placeholder': '标签'
            }),
            'idc_name':forms.Select(attrs={
                'class':'form-control select2'
            }),
            'ssh_user':forms.SelectMultiple(attrs={
                'class': 'form-control select2', 'data-placeholder': '用户'
            }),
            'comment':forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }

        help_texts = {
            'name': '* required',
            'ip': '* required',
            'port': '* required',
        }



class IdcForm(forms.ModelForm):

    class Meta:
        model = IDC
        fields = ('name','type','address','contack_name','contack_phone','contack_qq','contack_mail','bandwidth')
        widgets = {
            'name':widgets.Input(attrs={
                'class':'form-control'
            }),
            'type':forms.Select(attrs={
                'class':'form-control select2'
            }),
            'address':widgets.Input(attrs={
                'class':'form-control'
            }),
            'contack_phone':widgets.Input(attrs={
                'class':'form-control'
            }),
            'contack_name':widgets.Input(attrs={
                'class':'form-control'
            }),
            'contack_qq':widgets.Input(attrs={
                'class':'form-control'
            }),
            'contack_mail':widgets.EmailInput(attrs={
                'class':'form-control'
            }),
            'bandwidth':widgets.Input(attrs={
                'class':'form-control'
            }),


        }

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name','remark')
        widgets = {
            'name': widgets.Input(attrs={
                'class': 'form-control'
            }),
            'remark': widgets.Textarea(attrs={
                'class': 'form-control'
            })
        }

class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ('name','remark')
        widgets = {
            'name': widgets.Input(attrs={
                'class': 'form-control'
            }),
            'remark': widgets.Textarea(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': '名称',
            'remark':'备注'
        }
