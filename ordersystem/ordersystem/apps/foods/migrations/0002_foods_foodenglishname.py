# Generated by Django 2.0 on 2020-03-11 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foods',
            name='foodEnglishName',
            field=models.CharField(default=None, max_length=100, verbose_name='英文菜名'),
        ),
    ]