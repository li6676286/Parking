from django.conf.urls import url

from company.views import CompanyView, CompaniesView, CompanyParkView, CompanyParkingView

urlpatterns = [
    url(r'^companies$', CompaniesView.as_view()),
    url(r'^companies/(?P<company_id>\w+)$', CompanyView.as_view()),
    url(r'^companies/(?P<company_id>\w+)/parkings$', CompanyParkView.as_view()),
    url(r'^companies/(?P<company_id>\w+)/parkings2$', CompanyParkingView.as_view())

]
