from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls.defaults import handler404

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('practise', views.practise, name='practise' ),
    path('movielist/', views.get_csv_file, name='index' ),
    path('wait/', views.wait_page),
    re_path('.*', views.handler500)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

