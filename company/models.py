import uuid

from django.db import models

from time_helper import datetime_to_timestamp


class Company(models.Model):

    company_id = models.CharField(primary_key=True, max_length=32, default=uuid.uuid4().hex)
    company_name = models.CharField(max_length=100, db_index=True)
    company_address = models.CharField(max_length=100, db_index=True,null=True)
    updated_time = models.DateTimeField(auto_now=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True,db_index=True, null=True)

    class Meta:
        db_table = 'company'

    def detail_info(self):
        return {
            'company_id': self.company_id,
            'company_name': self.company_name,
            'company_address':self.company_address,
            'updated_time':datetime_to_timestamp(self.updated_time),
            'created_time':datetime_to_timestamp(self.created_time)
        }
