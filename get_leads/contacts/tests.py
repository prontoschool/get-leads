from django.contrib.auth.models import User
from django.test import TestCase


from .forms import ContactForm
from .models import Contact
import requests

class ContactTest(TestCase):
    def test_contact_should_have_firstname_and_lastname_email_ip(self):
        contact = Contact()
        contact.firstname = 'Steve'
        contact.lastname = 'Roger'
        contact.email = 'example@prontotools.com'
        contact.ip = '192.168.1.1'
        contact.save()
        contact = Contact.objects.first()
        self.assertEqual(contact.firstname, 'Steve')
        self.assertEqual(contact.lastname, 'Roger')
        self.assertEqual(contact.email, 'example@prontotools.com')
        self.assertEqual(contact.ip, '192.168.1.1')


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

    def test_contact_post_should_save_data(self):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': 'example@prontotools.com'
        }
        response = self.client.post(self.url, data=data)
        contact = Contact.objects.first()
        self.assertEqual(contact.firstname, 'Dao')
        self.assertEqual(contact.lastname, 'Duan')
        self.assertEqual(contact.email, 'example@prontotools.com')

    def test_contact_submit_should_see_thankyou(self):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': 'example@prontotools.com'
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, 'Thank You!, Dao Duan. Email is example@prontotools.com. IP: 58.137.162.34', status_code=200)

    def test_contact_view_should_see_email_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input id="id_email" name="email" type="email" />',status_code=200)

    def test_contact_submit_invalid_input_should_not_see_thankyou(self):
        data = {
            'firstname': 'Dao',
            'lastname': 'Duan',
            'email': ''
        }
        response = self.client.post(self.url, data=data, follow=True)
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
        contact.firstname = 'Dao'
        contact.lastname = 'Duan'
        contact.email = 'example@prontotools.com'
        contact.save()
        url = '/contact/thankyou/'
        response = self.client.get(url)
        self.assertContains(response, 'Thank You!, Dao Duan. Email is example@prontotools.com', status_code=200)


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
        contact.email = 'example@prontotools.com'
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
        contact.save()

        response =  self.client.get('/admin/contacts/contact/')
        self.assertContains(response, '<div class="text"><a href="?o=3">Email</a></div>', status_code=200)


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

