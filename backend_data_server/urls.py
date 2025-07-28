from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("homepage/", include("homepage.urls")),
    path("", lambda request: redirect("/homepage/index/")), 
]
