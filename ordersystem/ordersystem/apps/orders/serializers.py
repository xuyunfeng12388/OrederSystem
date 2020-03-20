from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers

from foods.models import Foods
from ordersystem.utlis.exceptions import logger
from .models import DinnerTable, OrderInfo, OrderGoods


class DinnerTableSerializers(serializers.ModelSerializer):
    class Meta:
        model = DinnerTable
        fields = ('id', 'tableName', 'tableKey', 'status')
        read_only_fields = ('id', 'tableName', 'tableKey')


class OrderSettlementSerializer(serializers.ModelSerializer):
    """
    购物车商品数据序列化器
    """
    count = serializers.IntegerField(label='数量')

    class Meta:
        model = Foods
        fields = ('id', 'foodName', 'foodEnglishName', 'img', 'price', 'discountPrice', 'count')


class SaveOrderSerializer(serializers.ModelSerializer):
    """
    下单数据序列化器
    """

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'pay_method', 'comment')
        read_only_fields = ('order_id',)
        extra_kwargs = {
            'pay_method': {
                'write_only': True,
                'required': True
            },
            'comment': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        """
        保存订单
        """
        # 获取当前下单用户
        dinnertable = self.context['dinnertable']

        # 组织订单编号 20170903153611+user.id
        # timezone.now() -> datetime
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % dinnertable.tableKey)

        pay_method = validated_data['pay_method']
        comment = validated_data['comment'] if validated_data['comment'] else None

        # 生成订单
        with transaction.atomic():
            # 创建一个保存点
            save_id = transaction.savepoint()
            try:
                # 创建订单信息
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    tableKey=dinnertable,
                    total_count=0,
                    total_amount=Decimal(0),
                    # freight=Decimal(10),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['FINISHED'] if pay_method == 1 else OrderInfo.ORDER_STATUS_ENUM[
                        'UNPAID'],
                    comment=comment
                )
                # 获取购物车信息
                # 从购物车中获取用户勾选要结算的商品信息
                redis_conn = get_redis_connection('carts')
                # 获取hash数据
                redis_cart = redis_conn.hgetall('carts_%s' % dinnertable.tableKey)
                # 获取set数据{b'1', b'2'}
                cart_selected = redis_conn.smembers('selected_%s' % dinnertable.tableKey)

                # 将bytes类型转换为int类型
                cart = {}
                for food_id in cart_selected:
                    cart[int(food_id)] = int(redis_cart[food_id])
                # # 一次查询出所有商品数据
                # foods = Foods.objects.filter(id__in=cart.keys())

                # 处理订单商品
                sku_id_list = cart.keys()
                for foods_id in sku_id_list:
                    while True:
                        food = Foods.objects.get(id=foods_id)
                        sku_count = cart[food.id]

                        for category in food.foodCategory.all():
                            if int(category.id) == 1:
                                price = food.discountPrice
                            else:
                                price = food.price
                        # 累计订单基本信息的数据
                        order.total_count += sku_count  # 累计总数
                        order.total_amount += price  # 累计总额

                        # 保存订单商品
                        OrderGoods.objects.create(
                            order=order,
                            goods=food,
                            count=sku_count,
                            price=price,
                        )
                        # 更新成功
                        break
                # 更新订单的金额数量信息
                # order.total_amount += order.freight
                order.save()

            except serializers.ValidationError:
                raise
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                raise
            # 提交事务
            transaction.savepoint_commit(save_id)

            # 更新redis中保存的购物车数据
            pl = redis_conn.pipeline()
            pl.hdel('carts_%s' % dinnertable.tableKey, *cart_selected)
            pl.srem('selected_%s' % dinnertable.tableKey, *cart_selected)
            pl.execute()
            return order


class FoodsSerializers(serializers.ModelSerializer):
    foodCategory = serializers.StringRelatedField(many=True)

    class Meta:
        model = Foods
        fields = ('id', 'foodName', 'foodEnglishName', 'remark', 'price', 'discountPrice', 'img', 'foodCategory')
        read_only_fields = (
            'id', 'foodName', 'foodEnglishName', 'remark', 'price', 'discountPrice', 'img', 'foodCategory')


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = FoodsSerializers()

    class Meta:
        model = OrderGoods
        fields = ('goods', 'count', 'price', "evaluate", "score", "is_commented")
        read_only_fields = ('order_id',)


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    下单数据序列化器
    """
    order_goods = OrderGoodsSerializer(many=True)
    tableKey = serializers.StringRelatedField()

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'tableKey', 'total_count', "total_amount", "pay_method", "status", "comment", "order_goods")
        read_only_fields = ('order_id', 'tableKey', 'total_count', "total_amount", "pay_method", "status", "comment""order_goods")
