# Generated by Django 2.1.4 on 2018-12-20 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20181220_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='ip_asset_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.IP_Asset', verbose_name='所属IP段'),
        ),
    ]
