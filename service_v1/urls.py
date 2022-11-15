from django.urls import re_path, path
from service_v1.controllers.test_view import TheModelView, TheModelViewTwo


# Import Authentication and Authorization View Modules
from service_v1.views.auth.login_view import login_view 
from service_v1.views.auth.logout_view import logout_view
from service_v1.views.auth.register_view import register_view
from service_v1.views.admin.register_admin_view import register_admin_view
from service_v1.views.auth.refresh_token_view import refresh_token_view


# Import Universal View Modules
# profile features
from service_v1.views.universal.profile_view import profile_view
from service_v1.views.universal.edit_profile_view import edit_profile_view
from service_v1.views.universal.detail_product_view import detail_product_view
# product features
from service_v1.views.universal.show_products_view import show_products_view
# category features
from service_v1.views.universal.categories_views import categories_view


# Import Admin View Modules
# dashboard feature
from service_v1.views.admin.dashboard_view import dashboard_view
# category features
from service_v1.views.admin.add_category_view import add_category_view
# product features
from service_v1.views.admin.add_product_view import add_product_view
from service_v1.views.admin.edit_product_view import edit_product_view
from service_v1.views.admin.delete_product_view import delete_product_view
# order features
from service_v1.views.admin.show_order_view import show_order_view as admin_show_order
from service_v1.views.admin.approve_order_view import approve_order_view


# Import User View Modules
# location feature
from service_v1.views.user.add_location_view import add_location_view
from service_v1.views.user.show_location_view import show_location_view

# cart features
from service_v1.views.user.add_cart_view import add_cart_view
from service_v1.views.user.show_cart_view import show_cart_view
from service_v1.views.user.update_cart_view import update_cart_view
from service_v1.views.user.delete_cart_view import delete_cart_view


# order features
from service_v1.views.user.show_order_view import show_order_view as user_show_order

from service_v1.views.user.add_order_view import add_order_view

from service_v1.views.user.delete_order_view import delete_order_view as user_delete_order
from service_v1.views.admin.delete_order_view import delete_order_view as admin_delete_order


urlpatterns = [

    # Authentication and Authorization Endpoint
    path('login', login_view, name = "login endpoint"),
    path('register', register_view, name = "register endpoint"),
    path('register_admin', register_admin_view, name = "register endpoint"),
    path('refresh_token', refresh_token_view, name = "refresh token endpoint"),
    path('logout', logout_view, name = "logout endpoint"),

    path('add_location', add_location_view, name = "add location endpoint"),
    path('show_location', show_location_view, name = "show location endpoint"),

    # Universal Endpoint
    path('profile', profile_view, name = "profile endpoint"),
    path('edit_profile', edit_profile_view, name = "edit profile endpoint"),
    path('detail_product/<product_url>', detail_product_view, name = "detail product endpoint"),
    path('products/', show_products_view, name = "show products endpoint"),
    path('categories', categories_view, name = "categories endpoint"),
    

    # Admin Endpoint
    path('dashboard', dashboard_view, name = "admin dashboard endpoint"),
    path('add_category', add_category_view, name = "add category endpoint"),
    path('add_product', add_product_view, name = "add product endpoint"),
    path('edit_product/<product_url>', edit_product_view, name = "edit product endpoint"),
    path('delete_product/<product_url>', delete_product_view, name = "delete product endpoint"),


    # User Endpoint
    path('add_cart', add_cart_view, name = "add cart endpoint"),
    path('show_cart', show_cart_view, name = "show cart endpoint"),
    path('update_cart', update_cart_view, name = "update cart endpoint"),
    path('delete_cart', delete_cart_view, name = "delete product endpoint"),
    
    # Order Endpoint
    path('add_order', add_order_view, name = "add order endpoint"),

    path('show_order/admin', admin_show_order, name = "admin show order endpoint"),
    path('show_order/user', user_show_order, name = "user show order endpoint"),

    path('approve_order', approve_order_view, name = "approve order endpoint"),

    path('delete_order/admin', admin_delete_order, name = "admin delete order endpoint"),
    path('delete_order/user', user_delete_order, name = "user delete order endpoint"),

    path('themodel', TheModelView),
    path('themodel/<int:id>', TheModelViewTwo)
]