from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
from .views import InventoryView, index, checkoutpage, ToolDetailView, add_to_cart,remove_single_tool_from_cart, remove_tool_from_cart, OrderSummaryView,add_tools, contact
=======
from django.contrib.auth import views as auth_views
from .views import (InventoryView,
                    index,
                    CheckoutView,
                    ToolDetailView,
                    add_to_cart,
                    remove_single_tool_from_cart,
                    remove_tool_from_cart,
                    OrderSummaryView,
                    add_tools,
                    register,
                    profile,
                    update_profile,
                    project,
                    )
>>>>>>> 0f7079ddf71554f0bc08f19b30f10a457997402c



urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', update_profile, name='edit-profile'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('products/<slug>', ToolDetailView.as_view(), name='product'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-single-tool-from-cart/<slug>', remove_single_tool_from_cart, name='remove-single-tool-from-cart'),
    path('remove-tool-from-cart/<slug>', remove_tool_from_cart, name='remove-tool-from-cart'),
    path('add-tools/', add_tools, name='add-tools'),
<<<<<<< HEAD
	path('contact/', contact, name='contact'),
] 
=======
    path('project/', project, name='project'),
]
>>>>>>> 0f7079ddf71554f0bc08f19b30f10a457997402c

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
