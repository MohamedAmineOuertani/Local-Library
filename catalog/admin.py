from dataclasses import field
from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language



#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Language)
# admin.site.register(Author)
admin.site.register(Genre)

class BookInstanceInline(admin.TabularInline):
    model= BookInstance
    extra= 0

class BookInline(admin.TabularInline):
    model= Book
    extra=0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display= ( 'first_name', 'last_name', 'date_of_birth', 'date_of_Death' )
    fields= ['first_name', 'last_name', ('date_of_birth', 'date_of_Death')]
    inlines= [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display= ('title', 'author', 'display_genre')

    inlines= [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter= ('status', 'due_back')

    list_display= ('book', 'status', 'due_back', 'id', 'borrower') 
   
    fieldsets= (('Informations', {'fields':('book', 'imprint', 'id')}),
        ('Availablity', {'fields': ('status', 'due_back', 'borrower')}),
        )
    



