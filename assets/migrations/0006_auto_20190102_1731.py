# Generated by Django 2.1.4 on 2019-01-02 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_newassetapprovalzone_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='asset',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Asset'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Asset'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Asset'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Asset'),
        ),
    ]
