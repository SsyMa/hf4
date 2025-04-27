from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('pictures/', views.pictures, name='pictures'),
    path('pictures/image/<int:id>', views.image, name='image'),
    path('upload_image/', views.upload_image),
    path('delete_image/<int:id>', views.delete_image, name='delete_image')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)