from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("homepage/", include("homepage.urls")),
    path("demo/rest/api/", include("demo_rest_api.urls")),
    # Redirect sin slash inicial o usando reverse
    path("", lambda request: redirect("homepage/index/")),
    # Alternativa con reverse (requiere import de reverse)
    # path("", lambda request: redirect(reverse("index"))),
]
