# Generated by Django 5.2 on 2025-05-18 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_issue_created_at_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=20),
        ),
    ]
