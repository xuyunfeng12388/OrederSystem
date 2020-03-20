from django.db import models

# Create your models here.
from ordersystem.utlis.models import BaseModel


class FoodsCategory(BaseModel):
    """菜单类别"""
    categoryName = models.CharField(max_length=25, verbose_name='类别名称')
    sequence = models.IntegerField(verbose_name='类别排序', default=1)

    class Meta:
        db_table = 'tb_foods_category'
        verbose_name = '食物类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.categoryName


class Foods(BaseModel):
    """菜单"""
    foodName = models.CharField(max_length=50, verbose_name='菜名',  unique=True)
    foodEnglishName = models.CharField(max_length=100, verbose_name='英文菜名',  default=None)
    remark = models.CharField(verbose_name="菜名简介", max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='原价')
    discountPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='折扣价')
    img = models.ImageField(upload_to='foods', verbose_name='菜名图片', null=True, default=None)
    foodCategory = models.ManyToManyField(FoodsCategory, related_name="foods", verbose_name="从属类别",
                                          blank=True)

    class Meta:
        db_table = 'tb_foods'
        verbose_name = '食物清单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.foodName


# class FoodsDetail(BaseModel):
#     """菜单详情"""
#
#     FOOD_WEIGHT_ENUM = {
#         "BIG": 1,
#         "CENTER": 2,
#         "LITTER": 3,
#
#     }
#     FOOD_WEIGHT_CHOICES = (
#         (1, "大份"),
#         (2, "中份"),
#         (3, "小份"),
#     )
#
#     foods = models.ForeignKey(Foods, on_delete=models.PROTECT, verbose_name="食物")
#     foodsWeight = models.SmallIntegerField(choices=FOOD_WEIGHT_CHOICES, default=1, verbose_name="食物分量")
#     foodsWeight = models.SmallIntegerField(choices=FOOD_WEIGHT_CHOICES, default=1, verbose_name="食物口味")
#
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='原价')
#     discountPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='折扣价')
#     remark = models.CharField(verbose_name="食物简介", max_length=255)
#     img = models.ImageField(upload_to='foods', verbose_name='食物图片', null=True, default=None)
#
#
#
#     class Meta:
#         db_table = 'tb_foods'
#         verbose_name = '食物清单'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "%s" % self.foodName
