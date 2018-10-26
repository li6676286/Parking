
from django.test import TestCase, Client



# Create your tests here.
from parking.models import Parking


class CommentsTestView(TestCase):

    def setUp(self):
        super(CommentsTestView, self).setUp()

        Parking.objects.create( company_name="comment1")
        Parking.objects.create( company_name="comment2")
        Parking.objects.create( company_name="comment3")
        Parking.objects.create( company_name="comment4")
        Parking.objects.create( company_name="comment5")
        self.client = Client(enforce_csrf_checks=True)

    def test_CommentsView_get_noparm(self):
        response = self.client.get('/companies')
        print(response.content)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_CommentsView_post_noparm(self):
        data = {'company_name':'zmy','company_id':'469879e337be4664831ae1f2af62e205'}
        response = self.client.post('/companies',data)
        print(response.content)
        print(response.status_code)
        self.assertEqual(response.status_code, 201)
