from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
from typing import Optional


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
                "published_date": 2025
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Coding with Roby", "Great CS book", 5, 2023),
    Book(2, "Be Fast with FastAPI", "Coding with Roby", "Great book", 5, 2024),
    Book(3, "Master Endpoints", "Coding with Roby", "Good CS book", 5, 2025),
    Book(4, "HP1", "Author 1", "An average book", 2, 2020),
    Book(5, "HP2", "Author 2", "A nice book", 3, 2021),
    Book(6, "HP3", "Author 3", "A terrible book", 1, 2022)
]


@app.get("/books")
async def get_all_books():
    """
    Returns all books
    """
    return BOOKS

@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None


@app.get("/books/")
async def get_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # Convert request to Book object
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.get("/books/publish/")
async def get_book_by_published_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update-book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
