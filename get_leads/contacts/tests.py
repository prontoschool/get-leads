from django.test import TestCase

from .models import Contact


class ContactTest(TestCase):
    def test_contact_should_have_firstname_and_lastname(self):
        contact = Contact()
        contact.firstname = 'Steve'
        contact.lastname = 'Roger'
        contact.save()
        contact = Contact.objects.first()
        self.assertEqual(contact.firstname, 'Steve')
        self.assertEqual(contact.lastname, 'Roger')


class ContactAdminTest(TestCase):
    def test_contact_admin_page_should_return_302(self):
        url = '/admin/contacts/contact/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class ContactViewTest(TestCase):
    def setUp(self):
        self.url = '/contact/'

    def test_contact_view_should_return_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contact_view_should_see_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<form action="thankyou.html" method="post">', status_code=200)

    def test_contact_view_should_see_firstname_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input type="text" name="firstname">',status_code=200)

    def test_contact_view_should_see_lastname_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input type="text" name="lastname">',status_code=200)


class ThankyouViewTest(TestCase):
    def test_thankyou_view_should_return_200(self):
        url = '/contact/thankyou/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
