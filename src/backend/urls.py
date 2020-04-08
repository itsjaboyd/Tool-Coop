from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (view_inventory,
                    index,
                    CheckoutView,
                    ToolDetailView,
                    add_to_cart,
                    remove_single_tool_from_cart,
                    remove_tool_from_cart,
                    OrderSummaryView,
                    setup,
                    register,
                    profile,
                    update_profile,
                    project,
                    contact,
                    PreviousOrderSummaryView,
                    AdminOrderSummaryView,
                    AdminOrdersView,
                    checkin_tools
                    )


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='backend/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='backend/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', update_profile, name='edit-profile'),
    path('inventory/', view_inventory, name='inventory'),
    path('products/<slug>', ToolDetailView.as_view(), name='product'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-single-tool-from-cart/<slug>', remove_single_tool_from_cart, name='remove-single-tool-from-cart'),
    path('remove-tool-from-cart/<slug>', remove_tool_from_cart, name='remove-tool-from-cart'),
    path('setup/', setup, name='setup'),
    path('contact/', contact, name='contact'),
    path('project/', project, name='project'),
    path('previous-order-summary/<id>', PreviousOrderSummaryView.as_view(), name='previous-order-summary'),
    path('orders/', AdminOrdersView.as_view(), name='orders'),
    path('admin-order-summary/<id>', AdminOrderSummaryView.as_view(), name='admin-order-summary'),
    path('check-in-tools/<id>', checkin_tools, name='checkin')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
