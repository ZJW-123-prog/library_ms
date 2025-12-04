from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
