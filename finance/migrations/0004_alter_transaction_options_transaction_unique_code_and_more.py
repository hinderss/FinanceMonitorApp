# Generated by Django 5.1.3 on 2024-11-11 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_remove_card_card_number_remove_card_cvv_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AddField(
            model_name='transaction',
            name='unique_code',
            field=models.IntegerField(default=3123, verbose_name='Уникальный код услуги'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='finance.card', verbose_name='Карта'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Название платежа'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='Избранный платёж'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата операции'),
        ),
        migrations.DeleteModel(
            name='FavoriteTransaction',
        ),
    ]
