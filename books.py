from fastapi import Body, FastAPI


app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'science'}
]


@app.get('/books')
async def get_all_books():
    """
    Returns all books
    """
    return BOOKS


@app.get('/books/{book_title}')
async def get_book_by_title(book_title: str) -> dict:
    """
    Returns a book based on its title.
    :param book_title:
    :return: a dictionary with a book's information
    """
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {'error': 'Book cannot be found'}


@app.get('/books/')
async def get_books_by_category_query(category: str) -> list:
    """
    Returns a list of books based on their category.
    :param category: The category of the book
    :return: a list of books based on the category
    """
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get('/books/{book_author}')
async def get_books_by_author_category_query(book_author: str, category: str) -> list:
    """
    Returns a list of books based on their author and category.
    :param book_author: The author of the book
    :param category: The category of the book
    :return: a list of books based on the category
    """
    books_to_return = []
    for book in BOOKS:
        if (book.get('author').casefold() == book_author.casefold() and
                book.get('category').casefold() == category.casefold()):
            books_to_return.append(book)
    return books_to_return


@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


@app.get('/books/by_author/{author}')
async def get_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return
