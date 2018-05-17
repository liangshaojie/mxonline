
from django.conf.urls import url

from .views import CourseListView,CourseDetailView,CourseInfoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='courses_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='courses_detail'),
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name='courses_info'),
]