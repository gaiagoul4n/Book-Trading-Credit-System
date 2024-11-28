from myapp import app, db

if __name__ == "__main__":
    # Ensure tables are created before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)