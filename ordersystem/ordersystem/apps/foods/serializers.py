from rest_framework import serializers

from foods.models import FoodsCategory, Foods


class FoodsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodsCategory
        fields = ('id', 'categoryName')
        read_only_fields = ('id', 'categoryName')


class FoodsSerializers(serializers.ModelSerializer):
    foodCategory = serializers.StringRelatedField(many=True)

    class Meta:
        model = Foods
        fields = ('id', 'foodName', 'foodEnglishName', 'remark', 'price', 'discountPrice', 'img', 'foodCategory')
        read_only_fields = (
        'id', 'foodName', 'foodEnglishName', 'remark', 'price', 'discountPrice', 'img', 'foodCategory')
