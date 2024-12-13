import csv
import os
import requests
import re
from myapp import db, app
from myapp.models import Book

# Function to download an image from a URL
def download_image(url, filename, book_pics):
    """
    Downloads or reuses an image for a book cover.
    Returns the filename that should be used in the database.
    """
    # Ensure book_pics directory exists
    if not os.path.exists(book_pics):
        os.makedirs(book_pics)
    
    image_path = os.path.join(book_pics, filename)

    # If the image already exists, just return the filename
    if os.path.exists(image_path):
        print(f"Image {filename} already exists, reusing it")
        return filename
    
    # If not, try to download it
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Successfully downloaded new image: {filename}")
        return filename
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return "default.jpg"  # Use a default image for failed downloads
    

# Function to clean author names
def clean_author(author):
    # Remove anything in parentheses or brackets
    return re.sub(r"(\[.*?\]|\(.*?\))", "", author).split(",")[0].strip()

# Function to clean genres
def clean_genre(genre):
    # Remove brackets and extra spaces
    return genre.strip("[]").split(",")[0].strip()

# Function to process the dataset and populate the database
def process_books(csv_path):
    book_pics = os.path.join('myapp', 'static', 'book_pics') 
    books_added = 0
    books_skipped = 0

    # Ensure book_pics directory exists
    if not os.path.exists(book_pics):
        os.makedirs(book_pics)
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['title'].strip()
            author = clean_author(row['author'])
            genre = clean_genre(row['genres'])
            image_url = row['coverImg']
            
            # Create a safe filename from title
            image_filename = f"{re.sub(r'[^a-zA-Z0-9]', '_', title)}_{books_added+1}.jpg"

            # Check if book already exists in database
            existing_book = Book.query.filter_by(title=title, author=author).first()
            
            if existing_book:
                print(f"Skipping duplicate book: {title} by {author}")
                books_skipped += 1
                continue
            
            # Get or download the image
            final_image_filename = download_image(image_url, image_filename, book_pics)  # Changed from book_pics_dir
            
            # Add new book to database
            book = Book(
                title=title,
                author=author,
                genre=genre,
                picture=final_image_filename
            )
            db.session.add(book)
            books_added += 1
            
            # Commit every 50 books to avoid memory issues
            if books_added % 50 == 0:
                db.session.commit()
                print(f"Processed {books_added} books so far...")

        # Final commit for remaining books
        db.session.commit()
        print(f"\nFinished processing books:")
        print(f"Added: {books_added}")
        print(f"Skipped: {books_skipped}")
        print("Books have been successfully added to the database!")

if __name__ == '__main__':
    with app.app_context():  # Use the existing `app` directly
        csv_file_path = 'data/books_ds.csv'
        process_books(csv_file_path)
