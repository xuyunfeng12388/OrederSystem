# Generated by Django 2.0 on 2020-03-16 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200311_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_method',
            field=models.SmallIntegerField(choices=[(1, '现金'), (2, '支付宝'), (3, '微信')], default=1, verbose_name='支付方式'),
        ),
    ]
