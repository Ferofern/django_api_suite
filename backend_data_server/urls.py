from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("homepage/", include("homepage.urls")),
    path("demo/rest/api/", include("demo_rest_api.urls")),
    path("", lambda request: redirect("homepage/index/")),
    path('landing/api/', include('landing_api.urls'))
]
