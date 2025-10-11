from rest_framework import routers
from django.urls import path, include
from .views import (UserProfileViewSet, ProductImageViewSet, ReviewViewSet, CartItemViewSet,
                   CategoryListAPIView, CategoryDetailAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView,
                    ProductListAPIView, ProductDetailAPIView)

router = routers.DefaultRouter()
router.register(r'user', UserProfileViewSet)
router.register(r'product_image', ProductImageViewSet)
router.register(r'comment', ReviewViewSet)
router.register(r'cart_item', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='sub_category_list'),
    path('sub_category/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='sub_category_detail'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail')
]