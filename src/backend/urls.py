from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import inventory_list, index, checkoutpage, productpage

urlpatterns = [
    path('', index, name='index'),
    path('inventory/', inventory_list, name='inventory-page'),
    path('products/', productpage, name='product-page'),
    path('checkout/', checkoutpage, name='checkout-page'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)