from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(90), unique=True)
    author = db.Column(db.String(90))
    publisher = db.Column(db.String(90))

    def __repr__(self):
        return f"{self.book_name} - {self.author}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author':book.author, 'publisher':book.publisher}
        output.append(book_data)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name":book.book_name, "author": book.author, "publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['name'], description=request.json['description'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "book has been deleted"}