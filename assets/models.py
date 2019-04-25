from django.db import models
from ansible_api.models import AnsibleServerGroup
from accounts.models import CustomUser
import uuid
# Create your models here.


idc_type = (
    (0,"IDC机房"),
    (1,"公有云"),
    (2,"私有云"),
)



class IDC(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=20,verbose_name='机房名称')
    type = models.IntegerField(verbose_name="机房类型",choices=idc_type,blank=True,null=True)

    address = models.CharField(max_length=20,verbose_name='机房位置')
    contack_name = models.CharField(max_length=10,verbose_name='联系人')
    contack_phone = models.CharField(max_length=20,verbose_name='联系电话',blank=True, null=True)
    contack_qq = models.CharField(max_length=10,verbose_name='联系qq',blank=True, null=True)
    contack_mail = models.EmailField(verbose_name='联系邮箱',blank=True, null=True)
    bandwidth = models.CharField(max_length=10,verbose_name='机房带宽',blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    class Meta:
        verbose_name = 'IDC列表'
        verbose_name_plural = 'IDC列表'

    def __str__(self):
        return self.name


class Server(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(unique=True,max_length=20,verbose_name='主机名')
    ip = models.GenericIPAddressField(unique=True,verbose_name='IP地址')
    project = models.ManyToManyField('Project',blank=True,verbose_name='业务组')
    label = models.ManyToManyField('Label',blank=True,verbose_name='服务标签')
    # soft = models.ManyToManyField(to=Soft,blank=True,verbose_name='应用')
    is_active = models.BooleanField(default=True,verbose_name='使用状态')
    system = models.CharField(max_length=20,blank=True,verbose_name='操作系统')
    idc_name = models.ForeignKey(IDC,verbose_name='所属机房',on_delete=models.CASCADE)
    location = models.CharField(max_length=30, verbose_name='机架位置',blank=True, null=True)
    check_time = models.DateTimeField(auto_now_add=True,verbose_name="检查时间")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    mod_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")
    ssh_port = models.IntegerField(verbose_name="SSH端口",default=22)
    # ssh_user = models.CharField(verbose_name="连接用户名",max_length=20,blank=False,null=False,default="root")
    ssh_user = models.ManyToManyField('ServerUser',blank=True,verbose_name='用户')
    manufacturer = models.CharField(max_length=20,blank=True, verbose_name='厂商')
    productname = models.CharField(max_length=30,blank=True, verbose_name='产品型号')
    service_tag = models.CharField(max_length=80,blank=True, null=True, verbose_name='序列号')
    cpu_model = models.CharField(max_length=50,blank=True,verbose_name='CPU型号')
    cpu_nums = models.CharField(max_length=50,blank=True,verbose_name='CPU线程数')
    cpu_groups = models.CharField(max_length=50,null=True,blank=True,verbose_name='CPU物理核数')
    mem = models.CharField(max_length=100,blank=True,verbose_name='内存大小')
    disk = models.CharField(max_length=300,blank=True,verbose_name='硬盘大小')
    hostname = models.CharField(max_length=30,blank=True,verbose_name='主机名')
    ip2 = models.CharField(max_length=50,null=True,blank=True, verbose_name='其他IP地址')
    ansible_group = models.ManyToManyField(to=AnsibleServerGroup,blank=True,verbose_name='ansible组')
    services = models.ManyToManyField('Service',blank=True,verbose_name='应用')
    create_by = models.ForeignKey(CustomUser,verbose_name='创建用户',on_delete=models.CASCADE)
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name='备注')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '主机列表'
        verbose_name_plural = '主机列表'



class AssetOperationLog(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    host = models.ForeignKey("Server",verbose_name="主机ID",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="修改详情",null=True)

    def __str__(self):
        return "资产日志"
    class Meta:
        verbose_name = "资产日志"
        verbose_name_plural = "资产日志"

class Project(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=30,unique=True,verbose_name="名称")
    remark = models.TextField(null=True,blank=True,verbose_name="介绍")
    check_time = models.DateTimeField(auto_now_add=True,verbose_name="检查时间")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '业务名称'
        verbose_name_plural = '业务组'

class Label(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=30,unique=True)
    remark = models.TextField(null=True,blank=True)
    check_time = models.DateTimeField(auto_now_add=True,verbose_name="检查时间")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '服务标签'
        verbose_name_plural = '服务标签'

class Service(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=30,unique=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    describe = models.TextField(null=True,blank=True)
    modify_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '应用服务'
        verbose_name_plural = '应用服务'

class Crond(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=30,unique=True)
    describe = models.TextField(null=True,blank=True)
    create_by = models.ForeignKey(CustomUser,verbose_name='创建用户',on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

class ServerLog(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    host = models.ForeignKey("Server",verbose_name="主机ID",on_delete=models.CASCADE)
    create_by = models.ForeignKey(CustomUser,verbose_name='创建用户',on_delete=models.CASCADE)
    describe = models.TextField(null=True,blank=True)
    detail = models.CharField(max_length=30,blank=True,verbose_name='详细字段')

    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

class ServerUser(models.Model):
    SSH_PROTOCOL = 'ssh'
    RDP_PROTOCOL = 'rdp'
    PROTOCOL_CHOICES = (
        (SSH_PROTOCOL, 'ssh'),
        (RDP_PROTOCOL, 'rdp'),
    )
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    priority = models.IntegerField(default=10, verbose_name="优先权限")
    protocol = models.CharField(max_length=16, choices=PROTOCOL_CHOICES, default='ssh', verbose_name='协议')
    auto_push = models.BooleanField(default=True, verbose_name='Auto push')
    sudo = models.TextField(default='/bin/whoami', verbose_name='Sudo')
    shell = models.CharField(max_length=64,  default='/bin/bash', verbose_name='Shell')
