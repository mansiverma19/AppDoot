from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from android.api_views import AppViewSet
from user.urls import userrouter
from android.urls import approuter

router = DefaultRouter()
# router.register(r'apps', AppViewSet, basename='apps_view')
router.registry.extend(userrouter.registry)
router.registry.extend(approuter.registry)

# Define schema view for OpenAPI schema
openapi_schema_view = get_schema_view(
    title="AppDoot API",
    description="API for interacting with AppDoot project",
    version="1.0.0",
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'))),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/android/', include('android.urls')),
    path('api/v1/swagger-ui/', TemplateView.as_view(template_name='swagger_ui.html', extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('openapi-schema/', openapi_schema_view, name='openapi-schema'),
]
