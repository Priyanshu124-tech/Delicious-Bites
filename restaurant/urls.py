from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu, name='menu'),
    path('add_to_order/<int:item_id>/', views.add_to_order, name='add_to_order'),
    path('cart/', views.cart_view, name='cart'),
    path('order/bill/<int:order_id>/', views.order_bill, name='order_bill'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('manage/orders/', views.admin_orders, name='admin_orders'),
    path('manage/menu/', views.admin_menu, name='admin_menu'),
    path('manage/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('manage/menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('manage/menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('debug/', views.debug_view, name='debug'),  # Debug view
]
