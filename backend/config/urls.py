from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from api.views import CategorieViewSet, AnnonceViewSet

# Vue racine
def home(request):
    return JsonResponse({
        "status": "ok",
        "message": "Backend Django E-petites Annonces",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "auth_token": "/api/auth/token/",
            "auth_refresh": "/api/auth/token/refresh/"
        }
    })

router = DefaultRouter()
router.register(r'categories', CategorieViewSet)
router.register(r'annonces', AnnonceViewSet)

urlpatterns = [
    path('', home, name='home'),  # ✅ Route racine
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # ✅ Routes JWT corrigées
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]