from . import views
from django.urls import path
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chatapp'

urlpatterns = [
     path('chat/<int:recipient_id>/', views.chat, name='chat'),
     path('send_message/<int:recipient_id>/', views.send_message_recipient, name='send_message'),
     # path('send_messages/', views.send_message, name='sendmsg'),
    
]