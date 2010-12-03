"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from models import WebUser

class WebUserTest(TestCase):
    def test_can_set_name(self):
        user = WebUser(name="Emily")
        self.failUnlessEqual("Emily", user.name) 
        user.save()
        self.failUnlessEqual("Emily", WebUser.objects.get(name="Emily").name)



