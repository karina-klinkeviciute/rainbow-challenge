"""rainbow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django_otp.admin import OTPAdminSite
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import private_storage.urls
from rest_framework.routers import DefaultRouter
from challenge.urls import router as challenge_router
from joined_challenge.urls import router as joined_challenge_router
from joined_challenge.views.files import JoinedChallengeFileDetailView, JoinedChallengeFileUploadView, \
    JoinedChallengeFilesListView, ConcreteJoinedChallengeFilesListView, ConcreteJoinedChallengeFileUploadView
from joined_challenge.views.joined_challenge import QRCodeScanView
from results.urls import router as results_router
from news.urls import router as news_router
from message.urls import router as message_router
from results.views.balance import BalanceView

from user.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

from user.views import UserActivationView, PasswordResetView


class OTPAdmin(OTPAdminSite):
    pass

class AdminSiteEditors(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice, TOTPDeviceAdmin)
for model_cls, model_admin in admin.site._registry.items():
    admin_site.register(model_cls, model_admin.__class__)

router = DefaultRouter()

router.registry.extend(challenge_router.registry)
router.registry.extend(joined_challenge_router.registry)
router.registry.extend(results_router.registry)
router.registry.extend(news_router.registry)
router.registry.extend(message_router.registry)

urlpatterns = [
    path('/', include('django.contrib.flatpages.urls')),
    # path('admin/', admin_site.urls),
    # path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/user/', include('user.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(router.urls)),
    path('challenge/', include('challenge.urls')),
    path('activate/<uid>/<token>', UserActivationView.as_view(), name='user-activate'),
    path('password_reset/<uid>/<token>', PasswordResetView.as_view(), name='user-activate'),
    path('private-media/', include(private_storage.urls)),
    re_path('^api/joined_challenge_files/(?P<path>.*)$', JoinedChallengeFileDetailView.as_view()),
    path('api/joined_challenge_file_upload/', JoinedChallengeFileUploadView.as_view()),
    path('api/joined_challenge_file_list/<uuid>/', JoinedChallengeFilesListView.as_view()),
    path('api/concrete_joined_challenge_file_list/<challenge_type>/<uuid>/',
         ConcreteJoinedChallengeFilesListView.as_view()),
    path('api/concrete_joined_challenge_file_upload/',
         ConcreteJoinedChallengeFileUploadView.as_view()),
    path('api/qr_code_scan/',
         QRCodeScanView.as_view()),
    path('api/results/balance/',
         BalanceView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
