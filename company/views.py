import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views.py here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from company.forms import CompanyForm, CompanyGetForm
from company.models import Company


@method_decorator(csrf_exempt, name='dispatch')
class CompaniesView(View):

    def post(self, request):
        res = CompanyForm(request.POST)
        if not res.is_valid():
            return HttpResponse(status=422)
        company = Company.objects.create(company_name=res.data.get('company_name'))
        data = {'company_id':company.company_id,
                'company_name':company.company_name}
        return HttpResponse(json.dumps(data),status=201)

    def get(self, request):
        res = CompanyGetForm(request.GET)
        if not res.is_valid():
            return HttpResponse(status=422)
        if res.data.get('company_name'):
            company = Company.objects.filter(company_name__contains=res.data.get('company_name'))
        else :
            company = Company.objects.all()
        companies = []
        for _ in company:
            companies.append(_.detail_info())
        return HttpResponse(companies)


@method_decorator(csrf_exempt, name='dispatch')
class CompanyView(View):
    def get(self, request, company_id):
        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(json.dumps(company.detail_info()))

    def put(self, request, company_id):
        stream = request.body.decode()
        jsondata = json.loads(stream)
        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            return HttpResponse(status=404)
        company.company_name = jsondata['company_name']
        company.company_address = jsondata['company_address']
        company.save()
        return HttpResponse(status=204)

    def delete(self, request, company_id):
        Company.objects.filter(company_id=company_id).delete()
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name='dispatch')
class CompanyParkView(View):
    '''
    关联查询，根据公司id查询旗下所有停车场信息
    '''
    def get(self, request, company_id):
        try:
            company = Company.objects.get(company_id=company_id)
            parking = company.parking_company.all()
            parkings = []
            for _ in parking:
                parkings.append(_.detail_info())
        except Company.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(json.dumps(parkings))

@method_decorator(csrf_exempt, name='dispatch')
class CompanyParkingView(View):
    '''
    复杂查询，给定公司id，查询旗下停车场名称包含‘parking_name’，以及停车场名以‘parking_name2’开头的全部停车场信息
    '''
    def get(self, request, company_id):
        try:
            res = CompanyGetForm(request.GET)
            if not res.is_valid():
                return HttpResponse(status=422)
            q = Q()
            if res.data.get('parking_name') and res.data.get('parking_name2'):
                q &= (Q(parking_name__contains=res.data.get('parking_name')) | Q(parking_name__startswith=res.data.get('parking_name2')))
            company = Company.objects.get(company_id=company_id)
            parking = company.parking_company.filter(q)
            listl = []
            for _ in parking:
                listl.append(_.detail_info())
        except Company.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(json.dumps(listl))