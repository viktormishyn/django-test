from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
from django.core.exceptions import ValidationError


class FunctionalTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter hash here:', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn(
            '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):

    def test_home_homepage_template(self):
        # test if home.html template is used during the request to '/' route
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        # test if HashForm exists and it is valid
        form = HashForm(data={'text': 'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        # testing hashlib.sha256 function
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual(
            '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', text_hash)

    def saveHash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash.save()
        return hash

    def test_hash_object(self):
        # testing creating Hash models and saving them to db
        hash = self.saveHash()
        pulled_hash = Hash.objects.get(
            hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        # testing '/hash/<str:hash>' route
        hash = self.saveHash()
        response = self.client.get(
            '/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        # testing Hash object's hash field validation
        def badHash():
            hash = Hash()
            hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824kkkkkkkkkkkkkkkkk'
            # hash too long
            hash.full_clean()
        self.assertRaises(ValidationError, badHash)