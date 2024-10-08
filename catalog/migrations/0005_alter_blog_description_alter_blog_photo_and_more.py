# Generated by Django 5.0.7 on 2024-08-02 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_blog_buyer_alter_product_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Содержимое"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="photo/",
                verbose_name="Изображение (превью)",
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="title",
            field=models.CharField(max_length=150, verbose_name="Заголовок статьи"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="views_count",
            field=models.PositiveIntegerField(default=0, verbose_name="Просмотры"),
        ),
    ]
