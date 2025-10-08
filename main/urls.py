from django.urls import path
from main.views import show_main, create_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import edit_product
from main.views import delete_product, add_product_entry_ajax, product_list_ajax, show_json_by_id_ajax, edit_product_entry_ajax, delete_product_ajax
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<str:id>/', show_product, name='show_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),
    path('ajax/get-product-data/<uuid:id>/', show_json_by_id_ajax, name='get_product_json_ajax'),
    path('ajax/edit-product-entry/<uuid:id>/', edit_product_entry_ajax, name='edit_product_entry_ajax'),
    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('ajax/product-list/', product_list_ajax, name='product_list_ajax'),
    path('ajax/delete_product/<uuid:product_id>/', delete_product_ajax, name='delete_product_ajax'),
]