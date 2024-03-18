from django.conf.urls.static import static
from django.urls import path

from my_shop import settings
from shop import views

app_name = "shop"

urlpatterns = [
    path("", views.show_products, name="all_products"),
    path("<slug:category_slug>/", views.show_products, name="category_products"),
    path("<int:id>/<slug:slug>/", views.product_detail, name="details"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
