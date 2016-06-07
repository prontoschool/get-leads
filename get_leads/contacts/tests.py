from django.test import TestCase
from .models import Contact

# Create your tests here.
class ContactTest(TestCase):
	def test_contact_should_have_firstname_and_lastname(self):
		contact = Contact()
		contact.firstname = 'Steve'
		contact.lastname = 'Roger'
		contact.save()
		contact = Contact.objects.first()
		self.assertEqual(contact.firstname, 'Steve')
		self.assertEqual(contact.lastname, 'Roger')

