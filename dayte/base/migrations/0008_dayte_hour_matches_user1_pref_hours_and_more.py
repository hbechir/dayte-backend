# Generated by Django 4.2.5 on 2023-11-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_matches_user1_pref_days_matches_user2_pref_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayte',
            name='hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='matches',
            name='user1_pref_hours',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='matches',
            name='user2_pref_hours',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='matches',
            name='user1_pref_days',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='matches',
            name='user2_pref_days',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]