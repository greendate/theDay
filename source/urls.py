from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.my, name='my'),
    path('edit/', views.edit, name='edit'),
    path('user/<int:identity>/', views.user, name='user'),
    path('new_event/', views.new_event, name='new_event'),
    path('event/<int:event_id>', views.event, name='event'),
    path('accept/<int:event_id>', views.accept, name='accept'),
    path('upload/<int:event_id>', views.upload_to_gallery, name = 'image_upload'),
    path('posts/<int:event_id>', views.posts, name = 'posts'),
    path('like/<int:event_id>/<int:status_id>', views.like, name = 'like'),
    path('comment/<int:event_id>/<int:status_id>', views.comment, name = 'comment'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
