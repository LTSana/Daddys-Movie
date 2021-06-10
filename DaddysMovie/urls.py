"""DaddysMovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', include('pages.urls')),
    path('zeus/admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('movie/', include('movie.urls')),
    #path('token-auth/', jwt_views.TokenObtainPairView.as_view()), # WE ARE USING SESSIONS NOW NOT JWT
    #path('token-refresh/', jwt_views.TokenRefreshView.as_view()), # WE ARE USING SESSIONS NOW NOT JWT
    #path('token-verify/', jwt_views.TokenVerifyView.as_view()), # WE ARE USING SESSIONS NOW NOT JWT
]


admin.site.site_header = "Daddys Movie. Administration"
admin.site.site_title = "Daddys Movie. Administration"

""" handler404 = "pages.views.handler404"
handler403 = "pages.views.handler403"
handler500 = "pages.views.handler500" """
