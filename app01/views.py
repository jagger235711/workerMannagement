import json
from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app01 import forms
from app01 import models
from app01.models import Admin
from app01.utils.pagination import Pagination
from app01.utils.verification_code import generate_captcha


#############################部门管理##################################

# Create your views here.
def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()
    page_object = Pagination(queryset=queryset, request=request, )
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.gennerate_html(),
    }
    return render(request, "depart_list.html", context)


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, "depart_add.html")
    else:
        title = request.POST.get("title")
        print(title)
        models.Department.objects.create(title=title)
        return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    if request.method == "GET":
        uid = request.GET.get("uid")
        models.Department.objects.filter(id=uid).delete()
    return redirect("/depart/list/")


def depart_edit(request, uid):
    """编辑部门"""
    if request.method == "GET":
        row_object = models.Department.objects.get(id=uid)
        # print(depart)
        return render(request, "depart_edit.html", {"row_object": row_object})
    else:
        title = request.POST.get("title")
        # row_object = models.Department.objects.filter(id=uid).first()
        # print(title, row_object)
        models.Department.objects.filter(id=uid).update(title=title)
        # print(title, row_object)
        return redirect("/depart/list/")


##########################用户管理####################################
def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all()
    # try:
    #     queryset = models.UserInfo.objects.all()
    # except Exception as e:
    #     print(e)
    #     print(queryset)
    page_object = Pagination(queryset=queryset, request=request)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.gennerate_html(),
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all(),
        }
        return render(request, "user_add.html", context)
    else:
        title = request.POST.get("title")
        print(title)
        models.Department.objects.create(title=title)
        return redirect("/depart/list/")


def user_add_by_modelForm(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == "GET":
        form = forms.UserModelForm()
        return render(request, "user_add_by_modelForm.html", {"form": form})
    else:
        form = forms.UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/user/list/")
        else:
            return render(request, "user_add_by_modelForm.html", {"form": form})


def user_edit(request, uid):
    """
    编辑用户
    :param uid:
    :param request:
    :return:
    """
    row_object = models.UserInfo.objects.filter(id=uid).first()
    if request.method == "GET":
        form = forms.UserModelForm(instance=row_object)  # instance是一个实例对象，通常是从数据库中获取的。而data是一个字典，其中包含要提交的数据。
        return render(request, "user_edit.html", {"form": form})
    else:
        form = forms.UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/user/list/")
        else:
            return render(request, "user_edit.html", {"form": form})


def user_delete(request, uid):
    models.UserInfo.objects.filter(id=uid).delete()
    return redirect("/user/list/")


# ###################################靓号管理##################################
def prettynum_list(request):
    """
    靓号列表
    :param request:
    :return:
    """
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="13879027292", price=10, level=1, status=1)
    # print(request.GET)
    #
    # str="/?"+request.GET.urlencode()+"&page=2"
    # print(str)

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict = {"mobile__contains": search_data}

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request, queryset=queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.gennerate_html()
    # 分页功能实现
    # page_size = 10  # 单页显示数据条数
    # page = int(request.GET.get("page", 1))
    # start = (page - 1) * page_size
    # end = page * page_size
    # # print(start,end)
    #
    # # ** 表示字典解包(dict unpacking)
    # # ** 的作用就是将字典解包成filter()方法可以接受的关键字参数形式。
    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[page_object.start:page_object.end]
    # # print(queryset)

    # # 数据总条数
    # total_count = models.PrettyNum.objects.filter(**data_dict).count()
    #
    # # 总页数
    # # 计算总页数
    # # 总页数 = 数据总条数 / 每页显示的数据条数
    # # 向上取整
    # total_page_count, div = divmod(total_count, page_size)
    # if div:
    #     total_page_count += 1

    # # 向页面中生成页码
    # page_str_list = []
    # # 显示当前页面前后和五页
    # plus = 5
    # start_page = page - plus
    # end_page = page + plus
    # # 当前或后不足五页时不改变起始和中止页
    # if start_page < 1:
    #     start_page = 1
    #     end_page = 2 * plus + 1
    # if end_page > total_page_count:
    #     start_page = total_page_count - 2 * plus
    #     end_page = total_page_count
    #
    # # 首页
    # page_str_list.append(
    #     ' <li><a href="?page={}">首页</a></li>'.format(1))
    # # 上一页
    # if page > 1:
    #     page_str_list.append(
    #         ' <li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
    #             page - 1))
    # else:
    #     page_str_list.append(
    #         ' <li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(1))
    #
    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    #
    # # 下一页
    # if page < total_page_count:
    #     page_str_list.append(
    #         ' <li><a href="?page={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
    #             page + 1))
    # else:
    #     page_str_list.append(
    #         ' <li><a href="?page={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
    #             total_page_count))
    # # 尾页
    # page_str_list.append(
    #     ' <li><a href="?page={}">尾页</a></li>'.format(
    #         total_page_count))
    #
    # page_string = mark_safe("".join(page_str_list))  # 标记为安全才会被网页解析

    context = {
        "search_data": search_data,

        "queryset": page_queryset,  # 分完页的数据
        "page_string": page_string,  # 生成的页面
    }
    return render(request, "prettynum_list.html", context=context)


def prettynum_add(request):
    """
    添加靓号
    :param request:
    :return:
    """
    if request.method == "GET":
        form = forms.PrettyNumModelForm()
        return render(request, "prettynum_add.html", {"form": form})
    else:
        form = forms.PrettyNumModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/prettynum/list/")
        else:
            return render(request, "prettynum_add.html", {"form": form})


def prettynum_edit(request, nid):
    """
    编辑靓号
    :param request:
    :param nid:靓号id
    :return:
    """
    if request.method == "GET":
        prettynum = models.PrettyNum.objects.filter(id=nid).first()
        form = forms.AddPrettyNumModelForm(instance=prettynum)
        return render(request, "prettynum_edit.html", {"form": form})
    else:
        form = forms.AddPrettyNumModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/prettynum/list/")
        else:
            return render(request, "prettynum_edit.html", {"form": form})


def prettynum_delete(request, nid):
    """
    删除靓号
    :param request:
    :param nid: 靓号id
    :return:
    """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/prettynum/list/")


##############################管理员管理#################################
def admin_list(request):
    """
    靓号列表
    :param request:
    :return:
    """
    # user_info = request.session.get("user_info", "")
    # if not user_info:
    #     return redirect("/login/")

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict = {"username__contains": search_data}

    queryset = models.Admin.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset=queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.gennerate_html()

    context = {
        "search_data": search_data,
        "queryset": page_queryset,  # 分完页的数据
        "page_string": page_string,  # 生成的页面
    }
    return render(request, "admin_list.html", context=context)


def admin_add(request):
    """
       添加管理员
       :param request:
       :return:
       """
    if request.method == "GET":
        form = forms.AdminModelForm()
        return render(request, "base_add.html", {"form": form, "title": "添加管理员"})
    else:
        form = forms.AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request, "base_add.html", {"form": form, "title": "添加管理员"})


def admin_delete(request, uid):
    """
    删除管理员
    :param request:
    :param uid:
    :return:
    """
    models.Admin.objects.filter(id=uid).delete()
    return redirect("/admin/list/")


def admin_edit(request, uid):
    """
    编辑管理员
    :param request:
    :param uid:
    :return:
    """
    try:
        row_object = Admin.objects.get(id=uid)
    except:
        return redirect("/admin/list/")
    if request.method == "GET":
        form = forms.AdminAddModelForm(instance=row_object)
        return render(request, "base_add.html", {"form": form, "title": "编辑管理员"})
    else:
        form = forms.AdminAddModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request, "base_add.html", {"form": form, "title": "编辑管理员"})


def admin_reset(request, uid):
    """
    重置密码
    :param request:
    :param uid:
    :return:
    """
    try:
        row_object = Admin.objects.get(id=uid)
    except:
        return redirect("/admin/list/")
    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = forms.AdminResetModelForm()
        context = {
            "title": title,
            "form": form,
        }
        return render(request, "base_add.html", context=context)
    else:  # post
        form = forms.AdminResetModelForm(data=request.POST, instance=row_object)  # 修改密码时原来的对象也要带上，否则就是新建一个对象了
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request, "base_add.html", {"form": form, "title": title})


def index(request):
    return redirect("/depart/list/")


def account_login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == "GET":
        form = forms.LoginForm()
        context = {
            "form": form,
        }
        return render(request, "login.html", context=context)
    else:  # post
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():  # is_valid是验证表单有无错误。不能校验用户是否存在
            vcode = form.cleaned_data.pop("vcode")
            vcode_session = request.session.get("captcha_text", "")
            if vcode.upper() != vcode_session.upper():
                form.add_error("vcode", "验证码错误")
                return render(request, "login.html", {"form": form})
            # print(form.cleaned_data)
            user_object = models.Admin.objects.filter(**form.cleaned_data).first()
            if user_object is None:
                form.add_error("password", "用户名或密码错误")
                return render(request, "login.html", {"form": form})
            else:  # 用户验证成功，生成随机字符串写入cookie和session
                request.session["user_info"] = {
                    "user_id": user_object.id,
                    "user_name": user_object.username,
                }
                request.session.set_expiry(60 * 60 * 24 * 7)  # 设置session过期时间为7Day

                # request.session["user_id"] = user_object.id
                # request.session["user_name"] = user_object.username
                return redirect("/")
        else:
            return render(request, "login.html", {"form": form})


def account_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    request.session.clear()
    return redirect("/login/")


def account_regist(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # 保证数据库操作的原子性
                    user = form.save()
                    user_profile = Profile.objects.create(user=user, is_first_login=1)
                    login(request, user)
                    messages.success(request, "注册成功！")
                    return redirect("userWeb:index")
            except Exception as e:
                messages.error(request, str(e))

    else:
        form = RegistrationForm()

    context = {"register_form": form}

    if form.errors:
        context["error_form"] = form
        messages.error(request, "注册失败！")

    return render(request=request, template_name="userWeb/registration/register.html", context=context)


def account_reset(request):
    return None


def account_vcode(request):
    """
    生成图片验证码
    :param request:
    :return:
    """
    img, captcha_text = generate_captcha()
    request.session["captcha_text"] = captcha_text
    # 设置session超时
    request.session.set_expiry(60)
    print(captcha_text)
    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())

    # return HttpResponse("...")


#######################任务管理#############################
def task_list(request):
    """
    任务列表
    :param request:
    :return:
    """
    form = forms.TaskModelForm()
    query_set = models.Task.objects.all().order_by("-id")

    page_object = Pagination(request, queryset=query_set, page_size=4, plus=3)
    page_queryset = page_object.page_queryset
    page_string = page_object.gennerate_html()

    context = {
        "form": form,
        "task_list": page_queryset,
        "page_string": page_string,
    }
    return render(request, "task_list.html", context=context)


@csrf_exempt
def task_add(request):
    form = forms.TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
    else:
        data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict))


def task_delete(request):
    return None


def task_edit(request):
    return None


@csrf_exempt  # 装饰器 免除csrf认证
def task_ajax(request):
    # print(request.GET)
    print(request.POST)
    # return HttpResponse(json.dumps(request.POST))
    return JsonResponse(request.POST)


def order_list(request):
    return render(request, "order_list.html")