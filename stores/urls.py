from django.urls import path

from stores.views import ProductListView, CategoryListView, StoreListView

urlpatterns = [
    path('stores/', StoreListView.as_view(), name='stores-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
]