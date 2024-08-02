from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from pytils.translit import slugify

from catalog.models import Product, Buyer, Blog


class ProductListView(ListView):
    """Просмотр списка товаров"""
    model = Product

class ProductDetailView(DetailView):
    """Просмотр информации о конкретном товаре"""
    model = Product

class ContactCreateView(CreateView):
    """Просмотр страницы "Контакты"
    и сбор информации от пользователя, который оставил вопрос"""
    model = Buyer
    fields = ('name', 'phone', 'message',)
    success_url = reverse_lazy('catalog:home')

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
    fields = ('title', 'description', 'photo',)
    success_url = reverse_lazy('catalog:blog')

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
    fields = ('title', 'description', 'photo',)
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:detail_blog', args=[self.kwargs.get('pk')])
class BLogDeleteView(DeleteView):
    """
    Удаление публикации
    """
    model = Blog
    success_url = reverse_lazy('catalog:blog')


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
    return redirect(reverse('catalog:blog'))