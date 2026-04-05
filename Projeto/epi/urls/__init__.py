from django.urls import include, path


app_name = "epi"


urlpatterns = [
    path("", include("epi.urls.entregas")),
    path("", include("epi.urls.devolucoes")),
    path("", include("epi.urls.baixas")),
    path("", include("epi.urls.movimentacoes")),
]
