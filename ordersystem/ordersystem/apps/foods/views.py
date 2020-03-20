from django.db.models import Avg, Sum, Count, Max, Min
from django.shortcuts import render

# Create your views here.
from foods.models import FoodsCategory, Foods
from foods.serializers import FoodsCategorySerializers, FoodsSerializers
from ordersystem.utlis.baseview import BaseGenericAPIView
from ordersystem.utlis.pagination import StandardResultsSetPagination
from ordersystem.utlis.response_code import RET


class FoodsCategoryView(BaseGenericAPIView):
    queryset = FoodsCategory.objects.all()
    serializer_class = FoodsCategorySerializers

    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by("sequence")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return self.response_data(code=RET.OK, msg="成功", data=data.data, pagination=True)
        try:
            serializer = self.get_serializer(queryset, many=True)
            if serializer.data:
                return self.response_data(code=RET.OK, msg="成功", data=serializer.data, pagination=False)
        except Exception:
            return self.response_data(code=RET.NODATA, msg="成功")


class FoodsView(BaseGenericAPIView):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializers

    pagination_class = StandardResultsSetPagination

    def get(self, request, id):
        # aggregate 的用法
        food = Foods.objects.filter(foodCategory=id).aggregate(Avg("price"), Sum("price"), Max("price"), Min("price"),
                                                               Count("price"))
        print(food)

        price = FoodsCategory.objects.filter(id=id).aggregate(Max("foods__price"), Avg("foods__price"))
        print(price)

        foods = Foods.objects.values("foodName").annotate(Count('foodCategory'))
        print(foods, "foodName")
        # for i in foods:
        #     print(i.foodCategory__count)

        goods = FoodsCategory.objects.values("categoryName").annotate(foods_count=Count('foods')).order_by(
            "foods_count")
        print(goods, "1")

        foodscategory = FoodsCategory.objects.values("categoryName").annotate(Sum("foods__price")).filter(
            foods__price__sum__lt=30.00)
        print(foodscategory, "每个类别的菜品价格")

        foods_max_price = FoodsCategory.objects.values("categoryName").annotate(Min("foods__price"))
        print(foods_max_price, "最便宜的")

        queryset = Foods.objects.filter(foodCategory=id).order_by("id")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return self.response_data(code=RET.OK, msg="成功", data=data.data, pagination=True)
        try:
            serializer = self.get_serializer(queryset, many=True)
            if serializer.data:
                return self.response_data(code=RET.OK, msg="成功", data=serializer.data, pagination=False)
        except Exception:
            return self.response_data(code=RET.NODATA, msg="成功")
