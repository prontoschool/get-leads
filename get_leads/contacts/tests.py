from django.contrib.auth.models import User
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
        self.assertContains(response, '<form action="." method="post">', status_code=200)

    def test_contact_view_should_see_firstname_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input type="text" name="firstname">',status_code=200)

    def test_contact_view_should_see_lastname_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input type="text" name="lastname">',status_code=200)


    def test_contact_view_should_see_submit_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit">Submit</button>',status_code=200)


    def test_contact_view_should_see_contact_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Contact Form', status_code=200)

    def test_contact_post_should_save_data(self):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan'
        }
        response = self.client.post(self.url, data=data)
        contact = Contact.objects.first()
        self.assertEqual(contact.firstname, 'Dao')
        self.assertEqual(contact.lastname, 'Duan')

    def test_contact_submit_should_see_thankyou(self):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan'
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, 'Thank You!', status_code=200)

    def test_contact_view_should_see_email_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input type="text" name="email">',status_code=200)


class ThankyouViewTest(TestCase):
    def test_thankyou_view_should_return_200(self):
        url = '/contact/thankyou/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_thankyou_view_should_to_see_thankyou(self):
        url = '/contact/thankyou/'
        response = self.client.get(url)
        self.assertContains(response, 'Thank You!', status_code=200)


class ContactAdminTest(TestCase):
    def test_contact_admin_should_have_firstname_column(self):
        User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(
            username='admin',
            password='admin'
        )

        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=1">Firstname</a></div>', status_code=200)

    def test_contact_admin_should_have_lastname_column(self):
        User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(
            username='admin',
            password='admin'
        )

        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=2">Lastname</a></div>', status_code=200)
