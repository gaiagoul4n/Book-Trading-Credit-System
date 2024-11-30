import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from myapp import app, db, bcrypt
from myapp.forms import SignUpForm, LoginForm, BookForm, BooksForSaleForm, CheckByTitleForm, BuyBookForm
from myapp.models import User, Book, BooksForSale
from flask_login import login_user, current_user, logout_user, login_required
# from PIL import Image

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'gaiag'}
    return render_template('index.html', title = 'title', user = user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, credit=5)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/browse')
def browse():
    return render_template('browse.html')

#route for books.html - displays books so that user can select a previosuly posted book to sell if it exists in the database
@app.route('/books', methods=['GET', 'POST'])
def books():
    form = CheckByTitleForm()
    page = request.args.get('page', 1, type=int)  # Get the current page from query parameters
    books_query = Book.query  # Base query
    
    if form.validate_on_submit(): # If searching by title
        search_title = form.title.data.strip()
        search = f"%{search_title}%"
        books_query = books_query.filter(Book.title.ilike(search))  # Case-insensitive search

    books = books_query.paginate(page=page, per_page=32)  # Limit results to 32 books per page
    return render_template('books.html', form=form, books=books)

def save_picture(form_picture):
    picture_path = os.path.join(app.root_path, 'static/book_pics', form_picture.filename)
    output_size = (125, 125)
    form_picture.save(picture_path)

#route for a new book being posted for sale - picture is saved to database during this using the procedure save_picture
@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    book_form = BookForm()
    books_for_sale_form = BooksForSaleForm()
    book_id = request.args.get('book_id')  # Get book_id if passed from books.html
    pre_filled_book = None

    # Check if the user selected an existing book
    if book_id:
        pre_filled_book = Book.query.get(book_id)
        if pre_filled_book:
            # Pre-fill BookForm fields with existing book details
            book_form.title.data = pre_filled_book.title
            book_form.author.data = pre_filled_book.author
            book_form.genre.data = pre_filled_book.genre

    # Handle form submission
    if book_form.validate_on_submit() and books_for_sale_form.validate_on_submit():
        # Save picture only for new books
        if not pre_filled_book:
            picture_file = save_picture(book_form.picture.data)
            book = Book(
                title=book_form.title.data,
                author=book_form.author.data,
                genre=book_form.genre.data,
                picture=picture_file,
            )
            db.session.add(book)
            db.session.commit()
        else:
            book = pre_filled_book

        # Save sale-specific details
        book_for_sale = BooksForSale(
            price=books_for_sale_form.price.data,
            style=books_for_sale_form.style.data,
            condition=books_for_sale_form.condition.data,
            seller_id=current_user.id,
            book_id=book.id,
        )
        db.session.add(book_for_sale)
        db.session.commit()

        flash('Book posted for sale successfully!', 'success')
        return redirect(url_for('index'))

    return render_template(
        'sell.html',
        title='Post Book for Sale',
        book_form=book_form,
        books_for_sale_form=books_for_sale_form,
        pre_filled_book=pre_filled_book,
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#route for account page - has the queries for displaying the users past sales and purchases, and has the code for calculating total credits spent and total credits made
@app.route('/account')
@login_required
def account():
    purchases = db.session.query(BooksForSale, Book, User).filter(BooksForSale.buyer_id==current_user.id).join(Book, BooksForSale.book_id==Book.id).join(User, BooksForSale.seller_id==User.id).all()
    total_credits_spent = 0
    for book in purchases:
        total_credits_spent = total_credits_spent + book.BooksForSale.price
    pass
    sales = db.session.query(BooksForSale, Book,User).filter(BooksForSale.seller_id==current_user.id, BooksForSale.buyer_id!=None).join(Book, BooksForSale.book_id==Book.id).join(User, BooksForSale.buyer_id==User.id).all()
    total_credits_made = 0
    for book in sales:
        total_credits_made = total_credits_spent + book.BooksForSale.price
    pass
    return render_template('account.html', title='Account', purchases=purchases, sales=sales, total_credits_spent=total_credits_spent, total_credits_made=total_credits_made)

#buy route has query so that books can be displayed on buy.html that aren't posted by the current user and that have not already been sold
@app.route('/buy', methods=['GET', 'POST'])
def buy():
    books = db.session.query(BooksForSale, Book, User).filter(BooksForSale.seller_id!=current_user.id, BooksForSale.buyer_id==None).join(Book, BooksForSale.book_id==Book.id).join(User, BooksForSale.seller_id==User.id).all()
    return render_template('buy.html', title='Buy', books=books)

#once book is selected to be bought, buybook route ensures that user has enough credit to purchase it, and makes the changes to seller and buyer credit
@app.route('/buybook/<int:buying_book_id>', methods=['GET', 'POST'])
@login_required
def buybook(buying_book_id):
        form = BuyBookForm()
        if request.method=='POST':
            book = BooksForSale.query.filter(BooksForSale.id==buying_book_id).first()
            print(book)
            sellerUser = User.query.filter(book.seller_id==User.id).first()
            new_seller_credit = sellerUser.credit + book.price
            new_credit = current_user.credit - book.price
            if new_credit < 0:
                flash('Insufficient credit', 'danger')
                return redirect(url_for('index'))
            else:
                book.buyer_id = current_user.id
                current_user.credit = new_credit
                sellerUser.credit = new_seller_credit
                db.session.commit()
                flash('Purchase successful', 'success')
                return redirect(url_for('index'))
        book = db.session.query(BooksForSale, Book).join(Book).filter(BooksForSale.id==buying_book_id).first()
        return render_template('buybook.html', title='Buy book', book=book, credit=current_user.credit, form=form)
