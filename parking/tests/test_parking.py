
from django.test import TestCase


# Create your tests here.
from parking.models import Parking


class CommentsTestView(TestCase):

    def setUp(self):
        super(CommentsTestView, self).setUp()
        Parking.objects.create( parking_name="comment1")
        Parking.objects.create( parking_name="comment2")
        Parking.objects.create( parking_name="comment3")
        Parking.objects.create( parking_name="comment4")
        Parking.objects.create( parking_name="comment5")

    def test_CommentsView_get_noparm(self):
        response = self.client.get('/parkings')
        print(response.content)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_CommentsView_post_noparm(self):
        data = {'parking_name':'lxddd','parking_id':'469879e337be4664831ae1f2af62e205'}
        response = self.client.post('/parkings',data)
        print(response.content)
        print(response.status_code)
        self.assertEqual(response.status_code, 201)
