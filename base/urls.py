from django.urls import path
from . import views
urlpatterns = [
    path('', views.index_view, name="home-page"),
    path('add/<str:pk>', views.add_to_cart, name="add"),
    path('remove/<str:pk>', views.remove_from_cart, name="remove"),
    path('login/', views.login_view, name="login-page"),
    path('reject/<str:pk>', views.reject, name="reject"),
    path('approve/<str:pk>', views.approve, name="approve"),
    path('myorders/', views.my_orders_view, name="my-orders-page"),
    path('order-all/', views.order_all, name="order-all"),
    path('signup/', views.signup_view, name="signup-page"),
    path('logout/', views.logout_view, name="logout"),
    path('admin-page/', views.admin_view, name="admin-page"),
    path('admin-page/history', views.history_view, name="history-page"),
    path('admin-page/orders', views.orders_view, name="orders-page"),
    path('order-history/', views.order_history, name="order-history"),
]
