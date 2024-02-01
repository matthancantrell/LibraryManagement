from django.urls import path, re_path
from management import views

urlpatterns = [
    re_path(r'^$', views.view_organization_list, name='view_organization_list'),
    re_path(r'^view_organization_list/$', views.view_organization_list, name="view_organization_list"),
    re_path(r'^add_org/$', views.add_org, name="add_org"),
    re_path(r'^add_lib/$', views.add_lib, name="add_lib"),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^set_password/$', views.set_password, name='set_password'),
    re_path(r'^add_book/$', views.add_book, name='add_book'),
    re_path(r'^add_img/$', views.add_img, name='add_img'),
    re_path(r'^view_book_list/$', views.view_book_list, name='view_book_list'),
    re_path(r'^view_book/detail/$', views.detail, name='detail'),
    re_path(r'^view_library/detail/$', views.library_detail, name="library_detail"),
    re_path(r'^view_organization/detail/$', views.organization_detail, name="organization_detail")
]
