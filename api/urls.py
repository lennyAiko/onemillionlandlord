from django.urls import path
from . import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("properties/", views.PropertyList.as_view()),
    path("properties/<int:pk>", views.PropertyDetail.as_view()),
    path("clients/", views.ClientList.as_view()),
    path("clients/<int:pk>", views.ClientDetail.as_view()),
]

