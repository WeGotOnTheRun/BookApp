# Generated by Django 2.0.2 on 2018-02-16 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180216_1849'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='favourite_books',
            table='favourite_books',
        ),
        migrations.AlterModelTable(
            name='favouritecategory',
            table='FavouriteCategory',
        ),
        migrations.AlterModelTable(
            name='ratebook',
            table='RateBook',
        ),
    ]
