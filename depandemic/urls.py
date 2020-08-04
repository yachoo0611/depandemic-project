from . import views
from django.urls import path
app_name="depandemic"
urlpatterns = [
    path('', views.index, name='index'),
    #path('learn', views.learn ,name="learn"),
    #path('codeform', views.codeform, name="codeform"),
    #path('pro', views.pro ,name="pro"),
    #path('compare', views.compare,name="compare"),
]