from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from course_platform.views import *

user_service = UserOperationSet.as_view({"get": "list", "post": "update"})
course = CourseViewSet.as_view({"get": "list", "post": "create", "put": "update"})

API_V1 = [
    url(r'^register/', RegList.as_view(), name='register'),
    url(r'^login/', LogList.as_view(), name='login'),
    url(r'^user_service/', user_service, name='user_service'),
    url(r'^course/', course, name='course'),
]

API_VERSIONS = [url(r'^v1/', include(API_V1))]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(API_VERSIONS))
    # url(r'^js/(?P<filename>.*\.js)$', js, name='js'),
    # url(r'^css/(?P<filename>.*\.css)$', css, name='css'),
    # url(r'^$', home, name='home')
]
