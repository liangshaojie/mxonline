
from django.conf.urls import url

from .views import CourseListView

urlpatterns = [
    url(r'list/$', CourseListView.as_view(), name='courses_list'),
]