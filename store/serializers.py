from rest_framework import serializers
from .models import (UserProfile, Cart, Category, SubCategory,
                     Product, Review, ProductImage, CartItem, FavoriteItem, Favorite)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_image', 'category_name']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'sub_categories']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'product_image', 'product_type', 'avg_rating', 'count_people']

    def avg_rating(self, obj):
        return obj.avg_rating()

    def count_people(self, obj):
        return obj.count_people()


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'products']


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format('%d-%m-%Y'))
    user = UserProfileReviewSerializer()
    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'stars', 'created_date']


class ProductDetailSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, read_only=True)
    subcategory = SubCategoryListSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['product_name', 'subcategory', 'price', 'article_number',
                  'description', 'product_image', 'video', 'image',
                  'product_type', 'created_date', 'reviews', 'avg_rating', 'count_people']

    def avg_rating(self, obj):
        return obj.avg_rating()

    def count_people(self, obj):
        return obj.count_people()



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True,
                                                    source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True,

                                                    source='product')
    class Meta:
        model = FavoriteItem
        fields = ['id', 'product', 'product_id', ]




class FavoriteSerializer(serializers.ModelSerializer):
    favorites = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorites']



