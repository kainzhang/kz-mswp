from django.urls import path
from record import views

app_name = 'record'

urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('record_list/<int:difficulty>', views.record_list, name='record_list'),
    path('user_record/', views.user_record, name='user_record'),
    path('record_insert/', views.record_insert, name='record_insert')

]