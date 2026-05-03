from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the Task Manager API",
        "endpoints": ["/api/", "/api/users/", "/admin/"]
    })

urlpatterns = [
    path("", api_root, name="api-index"),
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("tasks.urls")),
]   