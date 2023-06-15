# Generated by Django 4.2.2 on 2023-06-15 09:25

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_manager_image_alter_produit_manager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='image',
            field=models.ImageField(null=True, upload_to=api.models.image_uoload_profile),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='image',
            field=models.ImageField(null=True, upload_to=api.models.image_uoload_profile),
        ),
        migrations.CreateModel(
            name='Favoris',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produit', to='api.produit')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='api.vendor')),
            ],
        ),
    ]
