# Generated by Django 2.2.3 on 2019-10-28 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oge2020', '0002_auto_20191028_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время ответа')),
                ('answer', models.TextField()),
                ('number_questions_in_variant', models.IntegerField(verbose_name='Количество всех вопросов в варианте на момент сдачи')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oge2020.Question', verbose_name='Вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
