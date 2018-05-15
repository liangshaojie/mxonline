
from django.conf.urls import url

from .views import CourseListView,CourseDetailView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='courses_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='courses_detail'),
]