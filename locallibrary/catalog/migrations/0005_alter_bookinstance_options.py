# Generated by Django 4.0.5 on 2022-07-01 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_rename_brrower_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'set book as returned'),)},
        ),
    ]
