from math import perm
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date 

# Create your models here.

# ///////////////////////////////////////////////////////////
# //   a Record is an Instance of a Model (entiter)        //
# //   each Model have a banch of fields                   // 
# //   as a result each Record have a banch of fields      //
# ///////////////////////////////////////////////////////////


class Genre (models.Model):
    """Model representing a book Genre. """
    name = models.CharField(max_length=200, help_text= "Enter a book genre (e.g sience Fiction)", verbose_name="Name of Genre")

    def __str__(self):
        """string representing the Modelobject. """
        return self.name

class Language (models.Model):
    name= models.CharField(max_length=100, help_text="Enter the language (e.g. Arabic, English) etc..")

    def __str__(self):
        return self.name

class Book (models.Model):
    """Model representing a book (but not a spesific copy of a book ). """
    title= models.CharField(max_length=200)


    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author= models.ForeignKey('Author', on_delete= models.SET_NULL, null=True)
        # on_delete= models.SET_NULL mean you can delete ana author without deleting the book it self
        # null = true means you can creat a book without an author

    Summary= models.TextField(max_length=9000, help_text='Enter a breaf description of the book')
    
    isbn= models.CharField("ISBN", max_length=13,unique= True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="select a genre for this book")

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True,  help_text="select the language for this book" )

    class Meta:   
        permissions =(("can_add_Book","Can add the book "),("can_change_book","Can change the book "),("can_delete_book","Can delete the book "))    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse ('book-detail', args=[str(self.id)])
    
    def get_id_update (self):
        return reverse('book-update', args=[self.id])

    def get_id_delete (self):
        return reverse('book-delete', args=[self.id])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ','.join (genre.name for genre in self.genre.all() [:3])
        
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can bre borrowed from library). """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text= 'Unique ID for this particular book across whole library' )
    book= models.ForeignKey('book', on_delete=models.RESTRICT, null=True)
    borrower= models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True)
 

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
        )
    status= models.CharField(
        max_length=1,
        choices= LOAN_STATUS,
        blank= True,
        default='m',
        help_text='Book avoailablitty', 
    )
    imprint=models.CharField(max_length=200 )
    due_back = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"), )
    
    @property
    def is_overdue(self):
        """Determines if the book is overdue based on
        due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    def __str__(self):
        """String for representing the Model object."""
        return f'Book N°[{self.id}] - " {self.book.title} " '
        
class Author (models.Model):
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    date_of_birth= models.DateField(null=True, blank=True)
    date_of_Death= models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering= ['last_name', 'first_name']
        permissions= (("can_add_author", "Can add author"),("can_change_author", "Can change author"), ("can_delete_author", "Can delete author"))

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""

        return reverse('author-detail', args=[ str(self.id)])

    def __str__(self):
        """String for representing the Model object."""

        return f'{ self.first_name } {self.last_name}'

    def get_id_update (self):
        return reverse('author-update', args=[self.id])

    def get_id_delete (self):
        return reverse('author-delete', args=[self.id])
    







