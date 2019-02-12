# Generated by Django 2.1.5 on 2019-02-11 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='port',
            name='port_asset',
        ),
        migrations.AddField(
            model_name='port',
            name='port',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='port_networkasset', to='assets.NetworkAsset', verbose_name='所属设备'),
        ),
    ]