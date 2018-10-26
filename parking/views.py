import json

from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views.py here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from company.forms import CompanyGetForm
from company.models import Company
from parking.forms import ParkingPostForm
from parking.models import Parking


@method_decorator(csrf_exempt, name='dispatch')
class ParkView(View):
    def post(self, request):
        res = ParkingPostForm(request.POST)
        if not res.is_valid():
            return HttpResponse(status=422)
        if res.data.get('company_id'):
            company = Company.objects.get(company_id=res.data.get('company_id'))
            park = Parking.objects.create(
                parking_name=res.data.get('parking_name'),
                company_id=company.company_id
            )
            data = {'parking_id':park.parking_id,
                'parking_name':park.parking_name,
                'company_id':park.company.company_id}
        else:
            park = Parking.objects.create(parking_name=res.data.get('parking_name'))
            data = {'parking_id': park.parking_id,
                    'parking_name': park.parking_name,
                    }
        return HttpResponse(json.dumps(data),status=201)

    def get(self, request):
        res = ParkingPostForm(request.GET)
        if not res.is_valid():
            return HttpResponse(status=422)
        if res.data.get('parking_name'):
            parking = Parking.objects.filter(parking_name__contains=res.data.get('parking_name'))
        else :
            parking = Parking.objects.all()
        parkings = []
        for _ in parking:
            parkings.append(_.detail_info())
        return HttpResponse(parkings)


@method_decorator(csrf_exempt, name='dispatch')
class ParkingView(View):
    def get(self,request,parking_id):
        try:
            parking = Parking.objects.get(parking_id=parking_id)
        except Parking.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(json.dumps(parking.detail_info()))

    def put(self, request, parking_id):
        stream = request.body.decode()
        jsondata = json.loads(stream)
        try:
            parking = Parking.objects.get(parking_id=parking_id)
        except Parking.DoesNotExist:
            return HttpResponse(status=404)
        parking.parking_name = jsondata['parking_name']
        parking.parking_address = jsondata['parking_address']
        parking.save()
        return HttpResponse(status=204)

    def delete(self, request, parking_id):
        try:
            Parking.objects.get(parking_id=parking_id).delete()
        except Parking.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name='dispatch')
class ParkingCompanyView(View):
    '''
    关联查询，可以查询停车场所属公司信息
    '''
    def get(self,request,parking_id):
        try:
            parking = Parking.objects.get(parking_id=parking_id)
            company = parking.company.detail_info()
        except Parking.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(json.dumps(company))

