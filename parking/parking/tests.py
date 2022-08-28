from django.test import Client, RequestFactory


class BaseTestCaseSetup(object):
    def setUp(self):
        self.client = Client()
        self.rf = RequestFactory()
