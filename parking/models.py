import uuid

from django.db import models

from time_helper import datetime_to_timestamp


class Parking(models.Model):
    parking_id = models.CharField(primary_key=True, max_length=32, default=uuid.uuid4().hex)
    parking_name = models.CharField(max_length=100, db_index=True)
    parking_address = models.CharField(max_length=100, db_index=True,null=True)
    updated_time = models.DateTimeField(auto_now=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True,db_index=True, null=True)
    company = models.ForeignKey(
        'company.Company',
        related_name='parking_company',
        on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = 'parking'

    def detail_info(self):
        return {
            'parking_id': self.parking_id,
            'parking_name': self.parking_name,
            'parking_address':self.parking_address,
            'updated_time':datetime_to_timestamp(self.updated_time),
            'created_time':datetime_to_timestamp(self.created_time),
            'parking_company': self.company.company_name if self.company else None
        }