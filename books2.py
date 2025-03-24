from fastapi import FastAPI


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


BOOKS = [
    Book(1, "Computer Science Pro", "Coding with Roby", "Great CS book", 5),
    Book(2, "Be Fast with FastAPI", "Coding with Roby", "Great book", 5),
    Book(3, "Master Endpoints", "Coding with Roby", "Good CS book", 5),
    Book(4, "HP1", "Author 1", "An average book", 2),
    Book(5, "HP2", "Author 2", "A nice book", 3),
    Book(6, "HP3", "Author 3", "A terrible book", 1)
]


@app.get('/books')
async def get_all_books():
    """
    Returns all books
    """
    return BOOKS
