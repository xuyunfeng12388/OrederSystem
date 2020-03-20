from django.db import models

from ordersystem.utlis.models import BaseModel


# Create your models here.

class DinnerTable(BaseModel):
    """餐桌"""

    TABLE_STATUS_EMU = {
        "有人": 1,
        "空闲": 2
    }

    TABLE_STATUS_CHOICES = (
        (1, "有人"),
        (2, "空闲")
    )

    tableName = models.CharField(max_length=25, verbose_name="餐桌名称")
    tableKey = models.IntegerField(verbose_name='餐桌代号', default=None, unique=True)
    status = models.SmallIntegerField(choices=TABLE_STATUS_CHOICES, default=2, verbose_name="餐桌状态")

    class Meta:
        db_table = 'tb_dinner_table'
        verbose_name = '餐桌信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.tableName


class OrderInfo(BaseModel):
    """
    订单信息
    """
    PAY_METHODS_ENUM = {
        "CASE": 1,
        "ALIPAY": 2,
        "WEICHAT": 3,
    }

    PAY_METHOD_CHOICES = (
        (1, "现金"),
        (2, "支付宝"),
        (3, "微信")
    )

    ORDER_STATUS_ENUM = {
        "EDIT": 1,
        "PREPARE": 2,
        "UNPAID": 3,
        "FINISHED": 4,
    }

    ORDER_STATUS_CHOICES = (
        (1, "可编辑"),
        (2, "正在备菜"),
        (3, "待支付"),
        (4, "已完成"),
        (5, "取消"),
    )

    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    tableKey = models.ForeignKey(DinnerTable, on_delete=models.PROTECT, verbose_name="餐桌代号")
    # address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="收获地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额")
    # freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运费")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")
    comment = models.CharField(default=None, verbose_name="订单备注", max_length=1024)

    class Meta:
        db_table = "tb_order_info"
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.order_id, self.tableKey)


class OrderGoods(BaseModel):
    """
    订单商品
    """
    SCORE_CHOICES = (
        (0, '0分'),
        (1, '20分'),
        (2, '40分'),
        (3, '60分'),
        (4, '80分'),
        (5, '100分'),
    )
    order = models.ForeignKey(OrderInfo, related_name='order_goods', on_delete=models.CASCADE, verbose_name="订单")
    goods = models.ForeignKey("foods.Foods", on_delete=models.PROTECT, related_name="order_foods", verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    evaluate = models.TextField(default="", verbose_name="评价信息")
    score = models.SmallIntegerField(choices=SCORE_CHOICES, default=5, verbose_name='满意度评分')
    # is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    is_commented = models.BooleanField(default=False, verbose_name='是否评价了')

    class Meta:
        db_table = "tb_order_goods"
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
