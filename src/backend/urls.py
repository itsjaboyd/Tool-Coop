from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .view import InventoryListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', InventoryListView.as_view(), name='inventory'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)