from django.db import models


class Category(models.Model):
    """
    Модель категории товаров
    """
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
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """
    Модель товара
    """
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
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = (
            "category",
            "name",
        )


class Buyer(models.Model):
    """
    Модель неавторизованного пользователя, задавшего вопрос в разделе "Контакты"'
    """
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'
        ordering = ('name',)

class Blog(models.Model):
    """
    Модель блога
    """
    title = models.CharField(
        max_length=150,
        verbose_name="Заголовок статьи",
    )
    slug = models.CharField(
        max_length=150,
        verbose_name='slug',
        blank=True,
        null=True,
    )

    description = models.TextField(
        verbose_name="Содержимое",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="photo/",
        blank=True,
        null=True,
        verbose_name="Изображение (превью)",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "публикации"
        ordering = (
            "title",
        )

class Version(models.Model):
    """
    Модель для версии продукта
    """
    product = models.ForeignKey(Product, related_name="versions", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Продукт", help_text="Выберите продукт",)
    version_number = models.CharField(max_length=10, verbose_name="Номер версии", help_text="Введите номер версии", null=True, blank=True,)
    version_name = models.CharField(max_length=100, verbose_name="Название версии", help_text="Введите название версии", null=True, blank=True,)
    is_version_active = models.BooleanField(default=False, verbose_name="Активная версия", help_text="является ли версия активной",)

    def __str__(self):
        return f"{self.name_version}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ("version_number", "version_name",)
