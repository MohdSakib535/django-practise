
"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from base import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from oopswithdjango import views as ov

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Data_view.as_view()), #get
    path('s/',views.snippet_view.as_view()), #get  #post
    path('sd/<int:pk>/',views.snippet_details.as_view(),name="snippet_details"),
    path('r/',views.Resource_view.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
    path('sentry-debug/', trigger_error),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('f',views.fun1),
    path('f1',views.MyAPIView.as_view()),
    path('export',views.ExportMovieInfoView.as_view()),

    # Poll Endpoints
    path('polls/', views.PollListCreateView.as_view(), name='poll-list-create'),
    path('polls/<int:pk>/', views.PollRetrieveUpdateView.as_view(), name='poll-retrieve-update'),
    path('polls/<int:pk>/history/', views.PollHistoryView.as_view(), name='poll-history'),

    # Choice Endpoints
    path('choices/', views.ChoiceListCreateView.as_view(), name='choice-list-create'),
    path('choices/<int:pk>/', views.ChoiceRetrieveUpdateView.as_view(), name='choice-retrieve-update'),
    path('choices/<int:pk>/history/', views.ChoiceHistoryView.as_view(), name='choice-history'),


    #oops with django
    path("op",ov.vehicle_data_created),
    path("vd",ov.vehicle_dashboard,name="vehicle_dashboard"),
    path('service/<str:vehicle_type>/<int:vehicle_id>/', ov.service_vehicle, name='service_vehicle'),
    path('schema-viewer/', include('schema_viewer.urls')), #for schema viewer
    path('silk/', include('silk.urls', namespace='silk'))

   
    
]






