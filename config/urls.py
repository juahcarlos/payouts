from django.http import JsonResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def custom_json_404(request, exception=None):
    return JsonResponse({'detail': 'Not found.'}, status=404)

handler404 = custom_json_404

schema_view = get_schema_view(
   openapi.Info(
      title="Payouts API",
      default_version='v1',
      description="API for managing payouts",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('payouts.api.urls')),
    re_path(r'^api/.*', lambda request: JsonResponse({'detail': 'Not found.'}, status=404)),
]
