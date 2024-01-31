from django.urls import path, re_path
from management import views

urlpatterns = [
    # path('', views.organization_list, name='organizations'),
    re_path(r'^$', views.index, name='homepage'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^set_password/$', views.set_password, name='set_password'),
    re_path(r'^add_book/$', views.add_book, name='add_book'),
    re_path(r'^add_img/$', views.add_img, name='add_img'),
    re_path(r'^view_book_list/$', views.view_book_list, name='view_book_list'),
    re_path(r'^view_book/detail/$', views.detail, name='detail'),
]
