from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import CompanyManagement,CompanyLogin

urlpatterns =[
    path("register/",CompanyManagement.as_view(), name="register company"),
    path("login/", CompanyLogin.as_view(), name="company login")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
