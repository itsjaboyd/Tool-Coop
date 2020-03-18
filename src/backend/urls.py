from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import InventoryListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', InventoryListView.as_view(), name='inventory'),
    path('contact/', views.contact, name='contact_us'),
    path('product/', views.product, name='product'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
