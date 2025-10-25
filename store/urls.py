from rest_framework import routers
from django.urls import path, include
from .views import (UserProfileViewSet, ProductImageViewSet, ReviewViewSet, CartItemViewSet,
                   CategoryListAPIView, CategoryDetailAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView,
                    ProductListAPIView, ProductDetailAPIView, RegisterView, CustomLoginView,
                    LogoutView, CartViewSet, FavoriteItemViewSet, FavoriteViewSet)



router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet)
router.register(r'product_image', ProductImageViewSet)
router.register(r'comment', ReviewViewSet)
router.register(r'cart_item', CartItemViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),

    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='sub_category_list'),
    path('sub_category/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='sub_category_detail'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('cart/', CartViewSet.as_view(), name='cart_detail'),
    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('favorite/', FavoriteViewSet.as_view(), name='favorite_detail'),
    path('favorite_item/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('favorite_item/<int:pk>/', FavoriteItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]











