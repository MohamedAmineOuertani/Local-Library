import datetime
import re

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, BookInstance, Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy 
from catalog.forms import RenewBookModelForm
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def index(request): 
    """view function for home page of site"""

    # Generate counts of some of the main objects
    num_books= Book.objects.count()
    num_instances= BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available= BookInstance.objects.filter(status__exact= 'a').count()
    #count for authors
    num_author= Author.objects.count()

    # The 'all()' is implied by default.
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits']= num_visits + 1

    context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_author': num_author,
        'num_visits': num_visits,
        'num_instances_Available': num_instances_available,
    }

    """ Render the HTML template index.html 
    with the data in the context variable"""
    return render(request, 'index.html', context=context)

class BookListView (generic.ListView):
    model=Book
    paginate_by=10

    def get_context_data(self, **kwargs):
        context= super(BookListView, self).get_context_data(**kwargs)
        context['some_data']= 'this is just some data'
        return context

class BookDetailView (generic.DetailView):
    model= Book
    paginate_by=5

class AuthorListView (generic.ListView):
    model=Author
    paginate_by= 10

class AuthorDetailView (generic.DetailView):
    model= Author
    paginate_by=5

class LoanedBooksByUserListView (LoginRequiredMixin,generic.ListView):

    """Generic class-based view listing 
    books on loan to current user."""

    model= BookInstance
    template_name= 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by= 10
    def get_queryset(self): 
        return BookInstance.objects.filter(borrower= self.request.user).filter(status__exact='o').order_by('due_back')
        
class LonedBooksListView (PermissionRequiredMixin,generic.ListView):
    model= BookInstance
    permission_required= ('catalog.can_mark_returned',)
    template_name= 'catalog/bookinstance_list_borrowed_staff.html'
    paginate_by= 10 
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@login_required
@permission_required ('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    # If this is a POST request then process the Form data
    
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding)
        form = RenewBookModelForm(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            book_instance.due_back= form.data['due_back']
            book_instance.save()

            # redirect to a new URL
            return HttpResponseRedirect(reverse('Loned-books'))

          # If this is a GET (or any other method) create the default form.    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm( initial= {'due_back': proposed_renewal_date})

    context={
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/renew_book_librarian.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'catalog/signup.html', {'form': form}) 

class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Author
    permission_required=('catalog.can_add_author',)
    fields = ['first_name','last_name', 'date_of_birth', 'date_of_Death']
    template_name= 'catalog/author_form.html'    

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author
    permission_required= ('catalog.can_change_author',)
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    template_name= 'catalog/author_form.html'    

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    permission_required= ('catalog.can_delete_author',)
    success_url= reverse_lazy('authors')
    template_name= 'catalog/author_confirm_delete.html'

class BookCreate(PermissionRequiredMixin,CreateView):
    model= Book
    permission_required=('catalog.can_add_Book')
    fields= ['title', 'author', 'Summary','isbn','genre','language']
    template_name="catalog/book_form.html"

class BookUpdate(PermissionRequiredMixin,UpdateView):
    model = Book
    permission_required=('catalog.can_change_book')
    fields= ['title', 'author', 'Summary','isbn','genre','language']
    template_name="catalog/book_form.html"

class BookDelete(PermissionRequiredMixin,DeleteView):
    model= Book
    permission_required= ('catalog.can_delete_book')
    success_url= reverse_lazy('books')
    template_name="catalog/book_confirm_delete.html"


    

