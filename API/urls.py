
from django.contrib import admin
from django.urls import path
from api.views import Check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Check, name='home')
]
