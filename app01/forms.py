from django import forms

from app01 import models
from app01.utils.encrypt import md5


class BaseForm(forms.Form):
    exclude_fields = []  # 不希望添加约束的字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 通过定义插件的属性达到约束的目的
            if name in self.exclude_fields:
                continue
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )


class BaseModelForm(forms.ModelForm):
    exclude_fields = []  # 不希望添加约束的字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 通过定义插件的属性达到约束的目的
            if name in self.exclude_fields:
                continue
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )


class UserModelForm(BaseModelForm):
    name = forms.CharField(label="姓名", min_length=3)  # 自定义约束

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        widgets = {
            # "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
            "creat_time": forms.DateInput(attrs={"type": "date"}),
        }


class AdminModelForm(BaseModelForm):
    """
    子类自定义字段、父类自定义字段、meta类、子类init方法、父类init方法执行顺序
    当创建ProductForm对象时,执行顺序是:

    首先执行自定义的name字段
    首先执行父类中定义的自定义字段
    然后执行子类中定义的自定义字段

    最后才是各自的__init__方法

    然后进入__init__方法进行初始化逻辑
    原因是在Python中,类属性和方法的定义要先于__init__方法执行。
    自定义字段实际上是定义在类范围内的属性,所以会先于__init__执行。
    而在__init__内部,就可以访问到之前定义的name字段了。
    所以ModelForm子类中确实是自定义字段语句先执行,然后再执行__init__中的初始化代码。

    如果父类和子类中都定义了Meta类,执行顺序是:

    首先执行父类的Meta类
    然后执行子类的Meta类
    最后执行各自的__init__方法
    原因是在Python中,类属性和方法的定义要先于__init__方法执行。
    Meta类是定义在类范围,所以会先于__init__执行。

    __init__方法在类初始化的时候执行
    这 Ensure 子类Meta可以覆盖父类Meta的配置。

    """

    # 定义字段达到约束的目的，同时可以定义插件
    password = forms.CharField(
        label="密码",
        min_length=6,
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        label="确认密码",
        min_length=6,
        widget=forms.PasswordInput,
    )  # 自定义约束

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        # 给字段添加插件达到约束的目的
        # widgets = {
        #     "password": forms.PasswordInput,
        # }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        md5_password = md5(password)
        # 判断新旧密码是否一致
        if md5_password == self.instance.password:
            # print(self.instance.password)
            raise forms.ValidationError("新旧密码相同")
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("两次密码不一致")
        return confirm_password  # 钩子方法被调用之后返回的值


class AdminAddModelForm(BaseModelForm):
    class Meta:
        model = models.Admin
        fields = [
            "username",
        ]


class AdminResetModelForm(AdminModelForm):
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]


class PrettyNumModelForm(BaseModelForm):
    # # 重写字段，添加自定义规则
    # mobile = forms.CharField(
    #     label="手机号",
    #     max_length=11,
    #     min_length=11,
    #     validators=[
    #         RegexValidator(
    #             regex=r'^1[3-9]\d{9}$',
    #             message='手机号格式错误', code='mobile_error'
    #         )])
    price = forms.IntegerField(label="价格", max_value=99999999999)

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    # 通过自定义方法对字段做校验
    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        if len(mobile) != 11:
            raise forms.ValidationError("手机号长度错误")
        if not mobile.isdigit():
            raise forms.ValidationError("手机号格式错误")
        if models.PrettyNum.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("手机号已存在")
        # 验证通过，用户输入的值返回
        return mobile


class AddPrettyNumModelForm(PrettyNumModelForm):
    mobile = forms.CharField(label="手机号", disabled=True)

    class Meta:
        model = models.PrettyNum
        fields = "__all__"


class LoginForm(BaseForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True,
    )
    vcode = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True,
    )

    def clean_password(self):
        return md5(self.cleaned_data["password"])


class TaskModelForm(BaseModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {"detail": forms.TextInput}


class OrderModelForm(BaseModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "user"]


class UploadForm(BaseForm):
    exclude_fields = ["img"]
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


class UploadModelForm(BaseModelForm):
    exclude_fields = ["img"]

    class Meta:
        model = models.City
        fields = "__all__"
