# Generated by Django 2.1.5 on 2019-02-10 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebay_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='site_id',
            field=models.IntegerField(choices=[(0, 'United States'), (2, 'Canada'), (3, 'Royaume-Uni'), (15, 'Australie'), (16, 'Autriche'), (23, 'Belgium (French)'), (71, 'France'), (77, 'Allemagne'), (100, 'eBay Motors'), (101, 'Italie'), (123, 'Belgium (Dutch)'), (146, 'Pays-Bas'), (186, 'Espagne'), (193, 'Suisse'), (196, 'Taïwan'), (201, 'Hong Kong '), (203, 'Inde'), (205, 'Irlande'), (207, 'Malaisie'), (210, 'Canada'), (211, 'Philippines'), (212, 'Pologne'), (216, 'Singapour'), (218, 'Suède'), (223, 'Chine')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='site_id',
            field=models.IntegerField(choices=[(0, 'United States'), (2, 'Canada'), (3, 'Royaume-Uni'), (15, 'Australie'), (16, 'Autriche'), (23, 'Belgium (French)'), (71, 'France'), (77, 'Allemagne'), (100, 'eBay Motors'), (101, 'Italie'), (123, 'Belgium (Dutch)'), (146, 'Pays-Bas'), (186, 'Espagne'), (193, 'Suisse'), (196, 'Taïwan'), (201, 'Hong Kong '), (203, 'Inde'), (205, 'Irlande'), (207, 'Malaisie'), (210, 'Canada'), (211, 'Philippines'), (212, 'Pologne'), (216, 'Singapour'), (218, 'Suède'), (223, 'Chine')]),
        ),
    ]