from myapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#user table holds all data about the users created upon signup
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    credit = db.Column(db.Integer, nullable=False)

    def __repr__ (self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.credit}')"

#book table holds general info of books posted for sale for the first time, so that they may be reused for a different user wishing to sell the same book
class Book(db.Model):
    __tablename__ = 'Book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(50))

    def __repr__ (self):
        return f"Book('{self.title}', '{self.author}', '{self.genre}', '{self.picture}')"

#booksforsale table holds the information of all books ever posted for sale
class BooksForSale(db.Model):
    __tablename__ = 'BooksForSale'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    style = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable=False)

    seller = db.relationship('User', foreign_keys=[seller_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    book = db.relationship('Book', foreign_keys=[book_id])

    def __repr__ (self):
        return f"BooksForSale('{self.price}', '{self.condition}', '{self.seller_id}', '{self.buyer_id}', '{self.book_id}')"
        
#didn't have time to implement a booklist but this is what the table would look like in models.py
# class Booklist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#
#     def __repr__ (self):
#         return f"Booklist('{self.user_id}', '{self.book_id}')"
