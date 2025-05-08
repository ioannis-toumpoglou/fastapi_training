"""
A test case used for training on the FastAPI framework
"""
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    """
    Class Book
    """
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    """
    Class BookRequest for validation
    """
    id: Optional[int] = Field(description="Not required", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1900, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Coding with Roby",
                "description": "A new book description",
                "rating": 5,
                "published_date": 2025,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Coding with Roby", "Great CS book", 5, 2023),
    Book(2, "Be Fast with FastAPI", "Coding with Roby", "Great book", 5, 2024),
    Book(3, "Master Endpoints", "Coding with Roby", "Good CS book", 5, 2025),
    Book(4, "HP1", "Author 1", "An average book", 2, 2020),
    Book(5, "HP2", "Author 2", "A nice book", 3, 2021),
    Book(6, "HP3", "Author 3", "A terrible book", 1, 2022),
]


@app.get("/books")
async def get_all_books():
    """
    Returns all books
    """
    return BOOKS


@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(gt=0)):
    """
    Returns book by ID
    :param book_id: the ID of book
    """
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/")
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    """
    Returns book by rating
    :param book_rating: the rating of book
    """
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    """
    Creates a new book
    :param book_request: BookRequest
    """
    # Convert request to Book object
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.get("/books/publish/")
async def get_book_by_published_date(published_date: int = Query(gt=1900, lt=2031)):
    """
    Returns book by date of publication
    :param published_date: the date the book(s) was published
    """
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


def find_book_id(book: Book):
    """
    Returns the ID of a book
    :param book: Book
    """
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update-book")
async def update_book(book: BookRequest):
    """
    Updates a book
    :param book: BookRequest
    """
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    """
    Deletes a book
    :param book_id: the ID of the target book
    """
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
