from import_export import resources

from .models import Book


class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        exclude = ("published_on",)
