from django.conf.urls import url

from parking.views import ParkView, ParkingView, ParkingCompanyView

urlpatterns = [
    url(r'^parkings$', ParkView.as_view()),
    url(r'^parkings/(?P<parking_id>\w+)$', ParkingView.as_view()),
    url(r'^parkings/(?P<parking_id>\w+)/company$', ParkingCompanyView.as_view())
]