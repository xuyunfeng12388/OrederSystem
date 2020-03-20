from decimal import Decimal

from django.shortcuts import render

from rest_framework.mixins import CreateModelMixin
# Create your views here.
from django_redis import get_redis_connection
from rest_framework.response import Response

from foods.models import Foods
from orders.models import DinnerTable, OrderInfo
from orders.serializers import DinnerTableSerializers, OrderSettlementSerializer, SaveOrderSerializer, \
    OrderInfoSerializer
from ordersystem.utlis.baseview import BaseGenericAPIView
from ordersystem.utlis.pagination import StandardResultsSetPagination
from ordersystem.utlis.response_code import RET


class TableVIew(BaseGenericAPIView):
    """桌号展示"""
    serializer_class = DinnerTableSerializers
    queryset = DinnerTable.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('id')
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
            return self.response_data(code=RET.NODATA, msg="桌号不存在")


class OrderinfoView(BaseGenericAPIView):
    """订单结算"""

    def get(self, request, id):
        try:
            dinnertable = DinnerTable.objects.get(tableKey=id)
        except DinnerTable.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        # 从购物车中获取用户勾选要结算的商品信息
        redis_conn = get_redis_connection('carts')
        # 获取hash数据
        redis_cart = redis_conn.hgetall('carts_%s' % dinnertable.tableKey)
        # 获取set数据{b'1', b'2'}
        cart_selected = redis_conn.smembers('selected_%s' % dinnertable.tableKey)

        cart = {}
        for food_id in cart_selected:
            cart[int(food_id)] = int(redis_cart[food_id])

        # 查询商品信息
        foods = Foods.objects.filter(id__in=cart.keys())
        for food in foods:
            food.count = cart[food.id]
        print(foods)
        # 运费
        # freight = Decimal('10.00')

        serializer = OrderSettlementSerializer(foods, many=True)
        return self.response_data(code=RET.OK, msg="成功", data=serializer.data, pagination=False)


class SaveOrderView(BaseGenericAPIView):

    def get(self, request, id):
        try:
            dinnertable = DinnerTable.objects.get(tableKey=id)
        except DinnerTable.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        order = OrderInfo.objects.filter(tableKey=dinnertable.id)
        serializer = OrderInfoSerializer(order, many=True)
        return self.response_data(code=RET.OK, msg="成功", data=serializer.data, pagination=False)

    def post(self, request, id):
        try:
            dinnertable = DinnerTable.objects.get(tableKey=id)
        except DinnerTable.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        order = OrderInfo.objects.filter(tableKey=id,status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).all()
        if order:
            serializer_order = OrderInfoSerializer(order[0])
            return Response({
                'code': RET.ORDERSEXIST,
                "msg": "订单已经存在，请完成支付",
                "data": serializer_order.data
            })
        # if dinnertable.status == 1:
        #     return self.response_data(code=RET.SOMEONE, msg="有人使用")
        try:
            serializer = SaveOrderSerializer(data=request.data, context={'dinnertable': dinnertable})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception:
            return self.response_data(code=RET.ORDERSERRORS, msg="订单异常")
        else:
            dinnertable.status = 1
            dinnertable.save()
            return self.response_data(code=RET.OK, msg="成功", data=serializer.data, pagination=False)

