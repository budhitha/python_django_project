# Generated by Django 4.0.3 on 2023-10-15 11:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Purchased', 'Purchased'),
                                                     ('Delivering ', 'Delivering'), ('Delivered', 'Delivered')],
                                            default='Pending', max_length=50, null=True)),
                ('delivery_datetime', models.DateTimeField(blank=True, null=True)),
                ('car_part', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='company.carparts')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
