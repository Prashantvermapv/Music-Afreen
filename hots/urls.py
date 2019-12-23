from django.urls import path
from . import views
#from . import views
app_name='hots'
urlpatterns = [
    path('',views.indexView,name='index'),
    path('details/<int:hots_id>/',views.detailView,name='detail')
    ]
