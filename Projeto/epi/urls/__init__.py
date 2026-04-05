from django.urls import include, path


app_name = "epi"


urlpatterns = [
    path("", include("epi.urls.entregas")),
]

