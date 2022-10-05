from django.urls import path     
from . import views
urlpatterns = [
    path('', views.show_wall),
    path('add_message', views.create_message),	  
    path('add_comment', views.create_comment),
    path('delete_msg', views.delete_msg),	  

]