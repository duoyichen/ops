# Generated by Django 2.1.4 on 2018-12-27 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0018_auto_20181227_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_code',
            field=models.CharField(max_length=128, unique=True, verbose_name='资产编码'),
        ),
    ]
