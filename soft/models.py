from django.db import models
import uuid
from users.models import CustomUser
from assets.models import Server
# Create your models here.

soft_status = (
    (0,'未安装'),
    (1,'正在安装'),
    (2,'安装出错'),
    (3,'已安装'),
    (4,'正在卸载'),
    (5,'卸载出错'),
    (5,'卸载完成'),
)

class Soft(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=20,verbose_name='软件名称')
    version = models.CharField(max_length=20,verbose_name='软件版本')
    describe = models.TextField(null=True,blank=True,verbose_name="描述")
    soft_icon = models.ImageField(upload_to="soft_icons/",verbose_name='软件ICON')
    create_by = models.ForeignKey(CustomUser,verbose_name='创建用户',on_delete=models.CASCADE)
    server = models.ManyToManyField(to=Server,blank=True,verbose_name='主机')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")



class ServerSoft(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    server = models.ForeignKey(Server,verbose_name='主机',on_delete=models.CASCADE)
    soft = models.ForeignKey(Soft,verbose_name='软件',on_delete=models.CASCADE)
    status = models.IntegerField(choices=soft_status,verbose_name='状态')
