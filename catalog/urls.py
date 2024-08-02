from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactCreateView, BlogListView, BlogCreateView, BlogUpdateView, BlogDetailView, BLogDeleteView, toggle_publish

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", ContactCreateView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("blog/", BlogListView.as_view(), name="blog"),
    path("blog/create", BlogCreateView.as_view(), name="blog_create"),
    path("detail_blog/<int:pk>/", BlogDetailView.as_view(), name="detail_blog"),
    path("update_blog/<int:pk>/", BlogUpdateView.as_view(), name="update_blog"),
    path("delete_blog/<int:pk>/", BLogDeleteView.as_view(), name="delete_blog"),
    path("activity/<int:pk>/", toggle_publish, name="toggle_activity"),

]
