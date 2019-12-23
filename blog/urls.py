from django.urls import path
from . import views
app_name='blog'
urlpatterns = [
    path('',views.indexView,name='index'),
    path('detail/<int:blog_id>/',views.detailView,name='detail'),
    path('add/',views.create_blog,name='create_blog')
    ]
