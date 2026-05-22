from django.urls import path
from rest_framework.routers import DefaultRouter

from stores.views import (
    ProductListView,
    CategoryListView,
    StoreListView,
    CategoryListViewSet,
    CategoryDetailView,
)

router = DefaultRouter()
router.register("admin/categories", CategoryListViewSet, basename="admin-categories")

urlpatterns = [
    path("stores/", StoreListView.as_view(), name="stores-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("products/", ProductListView.as_view(), name="product-list"),
]

urlpatterns += router.urls
