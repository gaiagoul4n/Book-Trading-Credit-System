import csv
import os
import requests
from myapp import db, app
from myapp.models import Book

# Function to download an image from a URL
def download_image(url, filename):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        image_path = os.path.join('myapp', 'static', 'book_pics', filename)
        with open(image_path, 'wb') as file:
            file.write(response.content)
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
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['title']
            author = clean_author(row['author'])
            genre = clean_genre(row['genres'])  # Clean the genre
            image_url = row['coverImg']
            image_filename = f"{title.replace(' ', '_')}.jpg"

            # Skip if book already exists in the database
            if Book.query.filter_by(title=title, author=author).first():
                print(f"Skipping duplicate book: {title} by {author}")
                continue

            # Download the cover image
            image_filename = download_image(image_url, image_filename)

            # Add the book to the database
            book = Book(title=title, author=author, genre=genre, picture=image_filename)
            db.session.add(book)

        db.session.commit()
        print("Books have been successfully added to the database!")

if __name__ == '__main__':
    with app.app_context():  # Use the existing `app` directly
        csv_file_path = 'data/books_ds.csv'
        process_books(csv_file_path)
