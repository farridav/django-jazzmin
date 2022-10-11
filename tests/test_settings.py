from jazzmin.settings import get_search_model_string


def test_get_search_model_string():
    # model name is always lower case
    assert get_search_model_string("books.Book") == "books.book"
    assert get_search_model_string("books.book") == "books.book"
    # the app name gets never touched
    assert get_search_model_string("Books.Book") == "Books.book"
    assert get_search_model_string("BookShelf.book") == "BookShelf.book"
