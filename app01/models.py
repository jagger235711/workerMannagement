from django.db import models


# Create your models here.
class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=32, verbose_name="标题")

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # creat_time = models.DateTimeField(verbose_name="入职时间") # 年月日时分秒
    creat_time = models.DateField(verbose_name="入职时间")  # 只包含年月日

    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

    # django中定义的约束
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    # id = models.CharField(primary_key=True, verbose_name="号码ID", max_length=16)
    # 允许为空加上 null=True,blank=True
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "等级1"),
        (2, "等级2"),
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)

    status_choices = (
        (1, "未占用"),
        (2, "已占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(
        verbose_name="密码",
        max_length=64,

    )

    def __str__(self):
        return self.username


class Task(models.Model):
    """任务表"""

    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    title = models.CharField(verbose_name="任务名称", max_length=64)
    detail = models.TextField(verbose_name="任务描述")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", to_field="id", on_delete=models.CASCADE)
    level = models.SmallIntegerField(verbose_name="任务等级", choices=level_choices, default=1)

    # create_time = models.DateTimeField(verbose_name="创建时间")

    def __str__(self):
        return self.title


class Order(models.Model):
    """订单表"""
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="订单名称", max_length=32)
    price = models.IntegerField(verbose_name="订单价格")

    status_choices = (
        (1, "未支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices, default=1)
    user = models.ForeignKey(verbose_name="下单用户", to="Admin", to_field="id", on_delete=models.CASCADE)
