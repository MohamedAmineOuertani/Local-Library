from attr import field
from django.test import TestCase
from catalog.models import Author,Book
# Create your tests here.
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls): # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author= Author.objects.get(id=1)
        field_label= author._meta.get_field('first_name').verbose_name
        max_length= author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)
        self.assertEqual(field_label, 'first name')
    
    def test_date_of_death_label(self):
        author= Author.objects.get(id=1)
        field_label= author._meta.get_field('date_of_Death').verbose_name
        self.assertEqual(field_label, 'Died' )
    
    def test_object_name_is_last_name_comma_first_name(self):
        author= Author.objects.get(id=1)
        expected_object_name= f'{author.first_name} {author.last_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author= Author.objects.get(id=1)#This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(),'/catalog/author/1')
        
class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='The secret')

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label= book._meta.get_field('title').verbose_name
        max_length= book._meta.get_field('title').max_length
        self.assertEqual(max_length,200)
        self.assertEqual(field_label, 'title')

    def test_Summery_label(self):
        book = Book.objects.get(id=1)
        field_label= book._meta.get_field('Summary').verbose_name
        max_length = book._meta.get_field('Summary').max_length
        self.assertEqual(field_label,'Summary')
        self.assertEqual(max_length,9000)
    
    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(),'/catalog/book/1')
    
    def test_get_id_update(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_id_update(),'/catalog/author/1/update/')
    
    def test_get_id_delete(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_id_delete(),'/catalog/author/1/delete/')
    
    def test_isbn_label(self):
        book= Book.objects.get(id=1)
        field_label= book._meta.get_field('isbn').verbose_name
        max_length= book._meta.get_field('isbn').max_length
        self.assertEqual(field_label, 'ISBN')
        self.assertEqual(max_length, 13)
    


    
