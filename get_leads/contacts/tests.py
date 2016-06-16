from mock import patch,call

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ContactForm
from .models import Contact
import requests


class ContactTest(TestCase):
    def test_contact_should_have_firstname_and_lastname_email(self):
        contact = Contact()
        contact.name = 'Steve Roger'
        contact.email = 'example@prontotools.com'
        contact.save()
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'Steve Roger')
        self.assertEqual(contact.email, 'example@prontotools.com')


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
        self.assertContains(response, '<input id="id_firstname" name="firstname" type="text" />',status_code=200)

    def test_contact_view_should_see_lastname_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input id="id_lastname" name="lastname" type="text" />',status_code=200)


    def test_contact_view_should_see_submit_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit">Submit</button>',status_code=200)


    def test_contact_view_should_see_contact_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Contact Form', status_code=200)

    @patch('contacts.views.requests.get')
    def test_contact_post_should_save_data(self, mock_get_requests):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': 'example@prontotools.com'
        }
        get_request = mock_get_requests.return_value
        get_request.json.return_value = {
            'ip': '58.137.162.34',
            'country': 'Thailand'
        }
        expect_calls = [
            call('https://api.ipify.org?format=json'),
            call('http://ip-api.com/json?fields=country')
        ]
        response = self.client.post(self.url, data=data)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'Dao Duan')
        self.assertEqual(contact.email, 'example@prontotools.com')
        self.assertEqual(contact.ip, '58.137.162.34')
        self.assertEqual(contact.country, 'Thailand')
        mock_get_requests.assert_has_calls(expect_calls)

    @patch('contacts.views.requests.get')
    def test_contact_submit_should_see_thankyou(self, mock_get_requests):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': 'example@prontotools.com'
        }
        expect_calls = [
            call('https://api.ipify.org?format=json'),
            call('http://ip-api.com/json?fields=country')
        ]
        get_request = mock_get_requests.return_value
        get_request.json.return_value = {
            'ip': '58.137.162.34',
            'country': 'Mar'
        }
        response = self.client.post(self.url, data=data, follow=True)
        mock_get_requests.assert_has_calls(expect_calls)
        self.assertContains(response, 'Thank You!, Dao Duan. Email is example@prontotools.com. IP: 58.137.162.34', status_code=200)

    def test_contact_view_should_see_email_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input id="id_email" name="email" type="email" />',status_code=200)

    @patch('contacts.views.requests.get')
    def test_contact_submit_invalid_input_should_not_see_thankyou(self, mock_get_requests):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': ''
        }
        expect_calls = [
            call('https://api.ipify.org?format=json'),
            call('http://ip-api.com/json?fields=country')
        ]
        get_request = mock_get_requests.return_value
        get_request.json.return_value = {
            'ip': 'x.x.x.x',
            'country': 'Mar'
        }
        response = self.client.post(self.url, data=data, follow=True)
        mock_get_requests.assert_has_calls(expect_calls)
        self.assertNotContains(response, 'Thank You!, Dao Duan. Email is example@prontotools.com', status_code=200)


class ThankyouViewTest(TestCase):
    def test_thankyou_view_should_return_200(self):
        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.email = 'example@prontotools.com'
        contact.save()
        url = '/contact/thankyou/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_thankyou_view_should_to_see_thankyou(self):
        contact = Contact()
        contact.name = 'Dao Duan'
        contact.email = 'example@prontotools.com'
        contact.save()
        url = '/contact/thankyou/'
        response = self.client.get(url)
        self.assertContains(response, 'Thank You!, Dao Duan. Email is example@prontotools.com', status_code=200)


class ContactAdminTest(TestCase):
    def test_contact_admin_should_have_name_column(self):
        User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(
            username='admin',
            password='admin'
        )

        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.email = 'example@prontotools.com'
        contact.ip = '58.137.162.34'
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=1">Name</a></div>', status_code=200)

    def test_contact_admin_should_have_email_column(self):
        User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(
            username='admin',
            password='admin'
        )

        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.email = 'burasakorn@prontomarketing.com'
        contact.ip = '58.137.162.34'
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=2">Email</a></div>', status_code=200)

    def test_contact_admin_should_have_ip_column(self):
        User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(
            username='admin',
            password='admin'
        )

        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.email = 'burasakorn@prontomarketing.com'
        contact.ip = '58.137.162.34'
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=3">Ip</a></div>', status_code=200)

    def test_contact_admin_should_have_country_column(self):
        User.objects.create_superuser('admin', 'admin@test.com', 'admin')
        self.client.login(
            username='admin',
            password='admin'
        )

        contact = Contact()
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.email = 'burasakorn@prontomarketing.com'
        contact.ip = '58.137.162.34'
        contact.country = 'Mar'
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=4">Country</a></div>', status_code=200)


class ContactFormTest(TestCase):
    def test_form_should_contain_all_defined_fields(self):
        form = ContactForm()
        self.assertTrue('firstname' in form.fields)
        self.assertTrue('lastname' in form.fields)
        self.assertTrue('email' in form.fields)

    def test_form_is_valid_with_valid_input(self):
        valid_data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': 'duan@pronto.com'
        }

        form = ContactForm(data=valid_data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_form_is_invalid_with_when_some_input_missing(self):
        invalid_data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': ''
        }

        form = ContactForm(data=invalid_data)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

