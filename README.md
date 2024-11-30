# School Bookstore

A second-hand bookstore web application designed for students at my secondary school to trade books using a credit-based system. This platform provides an easy, accessible way to share books, earn credits, and discover new reads—all without involving money.

---

## Features
- **Browse Books**: Explore a wide selection of books available for trade.
- **Sell Books**: Post your second-hand books for trade to earn credits.
- **Buy Books**: Use earned credits to purchase books from other students.
- **Credit-Based System**: No money involved—credits are used to buy and sell books.

- **Dynamic Book Dataset Integration**: The project utilizes a dataset of books to preload the system with a comprehensive catalog, including titles, authors, genres, and cover images.
- **Image Processing**: Automatically downloads and integrates book cover images from external URLs, ensuring a visually appealing user interface.

---

### Data Processing Workflow
To preload the system with a catalog of books, the project incorporates advanced data processing techniques:

1. **Dataset Integration**:
   - Utilized a dataset of books (sourced from [Goodreads BBE Dataset](https://zenodo.org/record/4265096)) containing thousands of entries.
   - Filtered the dataset to include only English-language books with 14,000+ reviews on goodreads.

2. **Genre Validation**:
   - Standardized genres to a predefined list to ensure consistency across the application.
   - Applied conditional logic to handle books with multiple genres or invalid genres.

3. **Image Processing**:
   - Implemented a script to download and save book cover images from URLs.
   - Applied fallback logic for cases where image downloads failed, ensuring seamless user experience.

4. **Database Integration**:
   - Leveraged SQLAlchemy to populate the database with processed book data.
   - Automated the creation of new entries, including title, author, genre, and cover image, into the SQLite database.

#### Technical Skills Demonstrated:
- **Data Cleaning and Transformation**: Extracted relevant fields and standardized data from a complex dataset.
- **API/HTTP Requests**: Automated the retrieval of external resources (book cover images) using the `requests` library.
- **Database Management**: Designed and populated relational database models using SQLAlchemy.
- **Error Handling**: Implemented robust error-handling mechanisms for invalid data and failed HTTP requests.

---

## How to Install and Run the Project

### Prerequisites
- **Python 3.7+** installed on your computer.
- **Git** installed to clone the repository.
  
### 1. Clone the Repository

### 2. Navigate to the Project Directory

### 3. Set Up a Virtual Environment

### 4. Install Dependencies
Use the `requirements.txt` file to install the required Python libraries:
pip install -r requirements.txt

### 5. Run the Application
1. Start the Flask development server:
   python3 run.py
2. Open your browser and visit:
   http://127.0.0.1:5000

---

## Technologies Used
- **Python**: Backend logic.
- **Flask**: Web framework for handling routes and dynamic content.
- **SQLite**: Database for storing user and book information.
- **Bootstrap**: Responsive front-end styling.
- **Iconify**: Icons for UI improvement.

---

## Future Features
- **Book Recommendations**: Get suggestions based on previously bought books.
- **Book List Management**: Create a personal list of books you want to read or purchase later.
- **Advanced Filters**: Filter the book catalog by genre, condition, or price range.
