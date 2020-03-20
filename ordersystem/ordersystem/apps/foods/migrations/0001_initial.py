# Generated by Django 2.0 on 2020-03-11 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='数据创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='数据修改时间')),
                ('foodName', models.CharField(max_length=50, unique=True, verbose_name='菜名')),
                ('remark', models.CharField(max_length=255, verbose_name='菜名简介')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='原价')),
                ('discountPrice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='折扣价')),
                ('img', models.ImageField(default=None, null=True, upload_to='foods', verbose_name='菜名图片')),
            ],
            options={
                'verbose_name': '食物清单',
                'verbose_name_plural': '食物清单',
                'db_table': 'tb_foods',
            },
        ),
        migrations.CreateModel(
            name='FoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='数据创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='数据修改时间')),
                ('categoryName', models.CharField(max_length=25, verbose_name='类别名称')),
                ('sequence', models.IntegerField(default=1, verbose_name='类别排序')),
            ],
            options={
                'verbose_name': '食物类别',
                'verbose_name_plural': '食物类别',
                'db_table': 'tb_foods_category',
            },
        ),
        migrations.AddField(
            model_name='foods',
            name='foodCategory',
            field=models.ManyToManyField(blank=True, related_name='foods', to='foods.FoodsCategory', verbose_name='从属类别'),
        ),
    ]
