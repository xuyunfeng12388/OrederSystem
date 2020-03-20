from django.conf.urls import url
from django.urls import path, re_path

from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    path(r'tables/', views.TableVIew.as_view()),


    re_path(r'orders/(?P<id>\d+)/settlement/', views.OrderinfoView.as_view()),

    re_path(r'orders/(?P<id>\d+)/info/', views.SaveOrderView.as_view()),
]
