# Generated by Django 5.1.1 on 2024-10-04 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteweb', '0006_command'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteweb.order'),
        ),
        migrations.AlterField(
            model_name='command',
            name='status',
            field=models.CharField(choices=[('en attente', 'en attente'), ('payée', 'payée'), ('expédiée', 'expédiée'), ('livrée', 'livrée')], max_length=100),
        ),
        migrations.AlterField(
            model_name='command',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]