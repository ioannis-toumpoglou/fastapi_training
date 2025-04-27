from fastapi import FastAPI
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

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Not required", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Coding with Roby",
                "description": "A new book description",
                "rating": 5,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Coding with Roby", "Great CS book", 5),
    Book(2, "Be Fast with FastAPI", "Coding with Roby", "Great book", 5),
    Book(3, "Master Endpoints", "Coding with Roby", "Good CS book", 5),
    Book(4, "HP1", "Author 1", "An average book", 2),
    Book(5, "HP2", "Author 2", "A nice book", 3),
    Book(6, "HP3", "Author 3", "A terrible book", 1)
]


@app.get("/books")
async def get_all_books():
    """
    Returns all books
    """
    return BOOKS


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    # Convert request to Book object
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
