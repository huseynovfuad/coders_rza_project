from rest_framework import serializers
from products.models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "fullname")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()


class ProductListSerializer(serializers.ModelSerializer):
    # total_price = serializers.FloatField(read_only=True)
    # category = CategorySerializer()
    # wishlist = WishlistSerializer(many=True)
    # wish_count = serializers.ReadOnlyField(source="wishlist.count")
    # wish_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ("wishlist", "name")
        extra_kwargs = {
            "user": {"read_only": True},
            "slug": {"read_only": True},
            "wishlist": {"read_only": True},
        }

    # def get_wish_count(self, obj):
    #     return obj.wishlist.count()


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["total_price"] = instance.price - (instance.discount_price or 0)
        repr_["wish_count"] = instance.wishlist.count()
        repr_["category"] = CategorySerializer(instance.category).data
        repr_["wishlist"] = WishlistSerializer(instance.wishlist.all(), many=True).data
        return repr_



class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("name", "description", "category", "price", "discount_price")
    
    
    def validate(self, attrs):
        price = attrs.get("price", None)
        if price <= 0:
            raise serializers.ValidationError({"error": "Qiymet 0 ve ya asagi ola bilmez"})
        return super().validate(attrs)


    def create(self, validated_data):
        print(validated_data)
        return Product.objects.create(**validated_data)


    def update(self, instance, validated_data):
        return Product.objects.filter(id=instance.id).update(**validated_data)