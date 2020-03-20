from django.db import models


class BaseModel(models.Model):
    """自定义模型基类"""
    # auto_now_add=True 数据第一次才会生成的时间
    create_time = models.DateTimeField(verbose_name="数据创建时间", auto_now_add=True)
    # 数据每次修改,都会保存修改时的数据
    update_time = models.DateTimeField(verbose_name="数据修改时间", auto_now=True)

    class Meta:
        abstract = True  # 定义该模型类为抽象模型类,不需要在迁移建表的时候进行建表操作


