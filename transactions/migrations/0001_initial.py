# Generated by Django 2.2 on 2019-04-10 20:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2019, 4, 10, 20, 42, 7, 404524))),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transactions.BaseTransaction')),
                ('sale_price', models.FloatField(blank=True, null=True)),
            ],
            bases=('transactions.basetransaction',),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transactions.BaseTransaction')),
                ('purchase_price', models.FloatField(blank=True, null=True)),
                ('retail_price_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='card_catalog.CardPrice')),
            ],
            bases=('transactions.basetransaction',),
        ),
    ]
