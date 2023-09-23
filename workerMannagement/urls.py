"""workerMannagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', views.index),
    path('login/', views.account_login, name="account_login"),
    path('logout/', views.account_logout, name="account_logout"),
    path('regist/', views.account_regist, name="account_regist"),

    path('verification_code/', views.account_vcode, name="account_vcode"),
    # path('reset/', views.reset),
    path('reset/', views.account_reset, name="account_reset"),

    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/delete/<int:uid>/', views.admin_delete),
    path('admin/edit/<int:uid>/', views.admin_edit),
    path('admin/reset/<int:uid>/', views.admin_reset),

    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/edit/<int:uid>/', views.depart_edit),

    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/add_by_modelForm/', views.user_add_by_modelForm),
    path('user/delete/<int:uid>/', views.user_delete),
    path('user/edit/<int:uid>/', views.user_edit),

    path('prettynum/list/', views.prettynum_list),
    path('prettynum/add/', views.prettynum_add),
    path('prettynum/delete/<int:nid>/', views.prettynum_delete),
    path('prettynum/edit/<int:nid>/', views.prettynum_edit),

    ######################任务管理##############################
    path('task/list/', views.task_list),
    path('task/add/', views.task_add),
    path('task/delete/<int:tid>/', views.task_delete),
    path('task/edit/<int:tid>/', views.task_edit),

    path('task/ajax/', views.task_ajax),

    # 订单管理
    path('order/list/', views.order_list),
    path('order/add/', views.order_add),
    path('order/delete/<int:orderId>/', views.order_delete),
    path('order/detail/<int:orderId>/', views.order_detail),
    path('order/edit/<int:orderId>/', views.order_edit),

    #统计信息
    path('chart/list/', views.chart_list),
    path('chart/bar/', views.chart_bar),
    path('chart/line/', views.chart_line),
    path('chart/pie/', views.chart_pie),


]
