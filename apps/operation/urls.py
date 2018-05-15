
from django.conf.urls import url

from .views import ChangeFavView

urlpatterns = [
    url(r'change_fav/$', ChangeFavView.as_view(), name='change_fav'),
]