from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_check/', views.login_check, name='login_check'),
    path('register_check/', views.register_check, name='register_check'),
    path('add_event/', views.add_event, name='add_event'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('edit_event/<int:id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:id>/',views.delete_event,name="delete_event"),
    path('edit_user/<int:id>/', views.edit_user,name="edit_user"),
    path('delete_user/<int:id>/',views.delete_user,name="delete_user"),
    path('user/<int:user_id>/', views.user_dashboard, name='user_dashboard'),
    path('create_event/<int:user_id>/', views.create_event, name='create_event'),
    path('accept_event/<int:id>/', views.accept_event, name='accept_event'),
    path('reject_event/<int:id>/', views.reject_event, name='reject_event'),
    path('upload_event_media/', views.upload_event_media, name='upload_event_media'),
    path('delete_media/<int:media_id>/', views.delete_media, name='delete_media'),
    path('view_events/', views.view_events, name="view_events")
]


