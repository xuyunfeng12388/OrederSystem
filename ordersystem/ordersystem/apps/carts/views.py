from django.shortcuts import render
from django.views import View
import json, pickle, base64
from django import http
from django_redis import get_redis_connection

from foods.models import Foods
from orders.models import DinnerTable
from ordersystem.utlis.response_code import RET
from ordersystem.utlis.baseview import BaseAPIView


# Create your views here.
class CartsView(BaseAPIView):
    """购物车"""

    def post(self, request, table):
        # 获取请求体中的sku_id, count
        food_id = request.data.get('food')
        count = request.data.get('count')
        selected = request.data.get('selected', True)
        # 校验
        if all([table, food_id, count]) is False:
            return self.response_data(code=RET.PARAMERR, msg="参数不全")

        try:
            foods = Foods.objects.get(id=food_id)
        except Foods.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="该菜本店没有")

        # 判断当餐桌是空闲
        try:
            dinnertable = DinnerTable.objects.get(tableKey=table)
        except Foods.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")
        # if dinnertable.status == 1:
        #     return self.response_data(code=RET.NODATA, msg="本餐桌有人使用")

        # 如果是登录用户存储购物车数据到redis
        # 创建redis连接对象
        redis_conn = get_redis_connection('carts')
        # 创建管道
        pl = redis_conn.pipeline()
        """
        hash: {sku_id_1: count, sku_id2: count}
        set: {sku_id_1, sku_id_2}
        
        """
        # hincrby()
        pl.hincrby('carts_%s' % dinnertable.tableKey, food_id, count)
        # pl.expire('carts_%s' % user.id, 30)

        # sadd()
        if selected:  # 只有勾选的才向set集合中添加
            pl.sadd('selected_%s' % dinnertable.tableKey, food_id)
        # pl.expire('selected_%s' % user.id, 30)
        # 执行管道
        pl.execute()
        # 响应
        # return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功'})
        return self.response_data(code=RET.OK, msg="添加购物车成功")

    def get(self, request, table):
        """购物车数据展示"""
        try:
            dinnertable = DinnerTable.objects.get(tableKey=table)
        except Foods.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        if dinnertable:
            """登录用户获取redis购物车数据
            hash: {sku_id_1: count, sku_id2: count}
            set: {sku_id_1, sku_id_2}
            """
            # 创建redis连接对象
            redis_conn = get_redis_connection('carts')
            # 获取hash数据
            redis_cart = redis_conn.hgetall('carts_%s' % dinnertable.tableKey)

            # 获取set数据{b'1', b'2'}
            selected_ids = redis_conn.smembers('selected_%s' % dinnertable.tableKey)
            # 将redis购物车数据格式转换成和cookie购物车数据格式一致  目的为了后续数据查询转换代码和cookie共用一套代码
            cart_dict = {}
            for sku_id_bytes, count_bytes in redis_cart.items():
                cart_dict[int(sku_id_bytes)] = {
                    'count': int(count_bytes),
                    'selected': sku_id_bytes in selected_ids
                }

            """
           {
               sku_id_1: {'count': 2, 'selected': True},
               sku_id_2: {'count': 2, 'selected': True}
           }
           """
            # 查询到购物车中所有sku_id对应的sku模型
            foods_qs = Foods.objects.filter(id__in=cart_dict.keys())
            cart_foods = []  # 用来装每个转换好的sku字典
            for food in foods_qs:
                sku_dict = {
                    'id': food.id,
                    'name': food.foodName,
                    'english_name': food.foodEnglishName,
                    'remark': food.remark,
                    'price': str(food.price),
                    'discount_price': str(food.discountPrice),
                    'default_image_url': food.img.url,
                    'count': int(cart_dict[food.id]['count']),  # 方便js中的json对数据渲染
                    'selected': str(cart_dict[food.id]['selected']),
                    'amount': str(food.price * int(cart_dict[food.id]['count'])),
                    'discount_amount': str(food.discountPrice * int(cart_dict[food.id]['count']))
                }
                cart_foods.append(sku_dict)

            return self.response_data(code=RET.OK, msg="成功", data=cart_foods, pagination=False)

    def put(self, request, table):
        """修改购物车数据"""
        # 接收前端传入 sku_id, count, selected
        food_id = request.data.get('food')
        count = request.data.get('count')
        selected = request.data.get('selected')
        # 校验
        if all([id, food_id, count]) is False:
            return self.response_data(code=RET.PARAMERR, msg="参数不全")

        try:
            food = Foods.objects.get(id=food_id)
        except Foods.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="该菜本店没有")

        # 判断当餐桌是空闲
        try:
            dinnertable = DinnerTable.objects.get(tableKey=table)
        except Foods.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        # 响应给前端修改后的sku数据
        cart_food = {
            'id': food.id,
            'name': food.foodName,
            'english_name': food.foodEnglishName,
            'remark': food.remark,
            'price': str(food.price),
            'discount_price': str(food.discountPrice),
            'default_image_url': food.img.url,
            'count': int(count),  # 方便js中的json对数据渲染
            'selected': selected,
            'amount': str(food.price * int(count)),
            'discount_amount': str(food.discountPrice * int(count))
        }

        # 用户修改redis购物车数据
        # 创建redis连接对象
        redis_conn = get_redis_connection('carts')
        pl = redis_conn.pipeline()

        # hset  # 覆盖hash中的数据
        pl.hset('carts_%s' % dinnertable.tableKey, food.id, count)
        # 判断selected是True还是False
        if selected:
            # 将勾选的sku_id存储到set集合
            pl.sadd('selected_%s' % dinnertable.tableKey, food.id)
        else:
            # 不勾选时,将sku_id从set集合中移除
            pl.srem('selected_%s' % dinnertable.tableKey, food.id)

        pl.execute()
        # 响应
        return self.response_data(code=RET.OK, msg="修改购物车数据成功", data=cart_food, pagination=False)

    def delete(self, request, table):
        """删除购物车数据"""
        # 接收sku_id
        food_id = request.data.get('food')
        # 校验
        try:
            food = Foods.objects.get(id=food_id)
        except Foods.DoesNotExist:
            return http.HttpResponseForbidden('sku不存在')

        # 判断当餐桌是空闲
        try:
            dinnertable = DinnerTable.objects.get(tableKey=table)
        except Foods.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        if dinnertable:
            # 登录操作redis数据
            # 创建redis连接对象
            redis_conn = get_redis_connection('carts')
            # 创建管道
            pl = redis_conn.pipeline()
            # 删除hash中的sku_id及count
            pl.hdel('carts_%s' % dinnertable.tableKey, food.id)
            # 删除set集合中的勾选
            pl.srem('selected_%s' % dinnertable.tableKey, food.id)
            pl.execute()
        return self.response_data(code=RET.OK, msg="成功")


class CartsSelectView(BaseAPIView):
    """购物车全选"""

    def put(self, request, id):
        selected = request.data.get('selected', False)
        # print(selected)
        # if not selected:
        #     # return http.HttpResponseForbidden('参数有误')
        #     return self.response_data(code=RET.PARAMERR, msg="参数有误")

        try:
            dinnertable = DinnerTable.objects.get(tableKey=id)
        except DinnerTable.DoesNotExist:
            return self.response_data(code=RET.NODATA, msg="本餐桌不存在")

        if dinnertable:
            """登录用户操作redis数据"""
            # 创建redis连接对象
            redis_conn = get_redis_connection('carts')
            # 获取到hash购物车数据{food_id: count}
            redis_cart = redis_conn.hgetall('carts_%s' % dinnertable.tableKey)
            # 判断当前是全选还是全不选
            if selected:
                # 如果是全选把hash中的所有food_id添加到set集合中
                redis_conn.sadd('selected_%s' % dinnertable.tableKey, *redis_cart.keys())
            else:
                # 如果取消全选,把hash中的所有food_id 从set集合中删除
                redis_conn.delete('selected_%s' % dinnertable.tableKey)  # 将指定key对应的数据直接删除

        return self.response_data(code=RET.OK, msg="成功")
