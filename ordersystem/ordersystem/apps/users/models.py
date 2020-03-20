from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户模型类"""

    class Meta:
        db_table = 'tb_ordersystem_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
