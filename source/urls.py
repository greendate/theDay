from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.my, name='my'),
    path('edit/', views.edit, name='edit'),
    path('user/<int:identity>/', views.user, name='user'),
    path('new_event/', views.new_event, name='new_event'),
    path('event/<int:event_id>', views.event, name='event'),
    path('accept/<int:event_id>', views.accept, name='accept'),
    path('list/<int:event_id>', views.list, name='list'),
]
