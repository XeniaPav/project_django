from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Buyer, Blog, Version
from catalog.services import get_categories_from_cache


class ProductListView(ListView):
    """Просмотр списка товаров"""

    model = Product


class ProductDetailView(DetailView, LoginRequiredMixin):
    """Просмотр информации о конкретном товаре"""

    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(self.request.POST)
        else:
            context_data["formset"] = ProductFormset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового товара
    """

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return redirect("catalog:product_detail", product.pk)
        # context_data = self.get_context_data()
        # formset = context_data['formset']
        # if formset.is_valid():
        #     formset.instance = self.object
        #     formset.save()
        #     return super().form_valid(form)
        # else:
        #     return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    def get_form_class(self):
        user = self.request.user
        user.save()
        if user == self.object.owner:
            return ProductForm
        if (
            user.has_perm("catalog.can_edit_product_description")
            and user.has_perm("catalog.can_edit_product_category")
            and user.has_perm("catalog.can_cancel_publication")
        ):
            return ProductModeratorForm
        raise PermissionDenied


class ContactCreateView(CreateView):
    """Просмотр страницы "Контакты"
    и сбор информации от пользователя, который оставил вопрос"""

    model = Buyer
    fields = (
        "name",
        "phone",
        "message",
    )
    success_url = reverse_lazy("catalog:home")


class BlogListView(ListView):
    """
    Просмотр списка публикаций
    """

    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """
    Просмотр конкретной публикации
    """

    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """
    Создание новой публикации
    """

    model = Blog
    fields = (
        "title",
        "description",
        "photo",
    )
    success_url = reverse_lazy("catalog:blog")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """
    Изменение публикации
    """

    model = Blog
    fields = (
        "title",
        "description",
        "photo",
    )
    success_url = reverse_lazy("catalog:blog")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:detail_blog", args=[self.kwargs.get("pk")])


class BLogDeleteView(DeleteView):
    """
    Удаление публикации
    """

    model = Blog
    success_url = reverse_lazy("catalog:blog")


def toggle_publish(request, pk):
    """
    Включение/отключение публикации
    """
    publish_item = get_object_or_404(Blog, pk=pk)
    if publish_item.is_published:
        publish_item.is_published = False
    else:
        publish_item.is_published = True

    publish_item.save()
    return redirect(reverse("catalog:blog"))
