# Generated by Django 3.2.16 on 2023-01-07 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='status',
            field=models.IntegerField(choices=[(0, 'Unpublished'), (1, 'Published')], default='Unpublished'),
        ),
    ]
