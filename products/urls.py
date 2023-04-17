from django.urls import path
from . import views

app_name = "products"


urlpatterns = [
    path("", views.index_view, name="index"),
    path("list/", views.product_list_view, name="list"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("basket/", views.basket_list_view, name="basket"),
    path("add-basket/", views.add_basket_view, name="add-basket"),
    path("detail/<id>/", views.product_detail_view, name="detail"),
    path("product-wish/", views.product_wish_view, name="product-wish"),
]