from django.urls import path
from .views import ProductList, CachedProductListView, Addproduct
urlpatterns = [

    path("normal_product",ProductList.as_view(),name='non_cached_product' ),
    path("cache_product", CachedProductListView.as_view(), name='cached_product'),
    path('addproduct/<int:number>/', Addproduct.as_view(),name="add_product")
]
