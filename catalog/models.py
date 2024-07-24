from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="photo/",
        blank=True,
        null=True,
        verbose_name="Изображение (превью)",
        help_text="Загрузите изображение товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию",
        null=True,
        blank=True,
        related_name="categories"
    )
    price = models.IntegerField(
        blank=True, null=True, verbose_name="Цена", help_text="Укажите цену товара"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    manufactured_at = models.DateField(
        verbose_name='Дата производства',
        help_text='Введите дату производства продукта',
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = (
            "category",
            "name",
        )
