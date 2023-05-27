from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/programing/Desktop/programing/library_for_books_Flask_sqllite/book-collection.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class Books(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f'<Book {self.title}>'

app.app_context().push()
db.create_all()




@app.route('/')
def home():
    # print(len(all_books["title"]))
    books = db.session.query(Books).all()
    return render_template('index.html', book = books)

@app.route("/edit<i>", methods=["GET", "POST"])
def edit_rating(i):
    books = db.session.query(Books).filter(Books._id == i)
    for i in books:
        name = i.title
        rating = i.rating
    
    if request.method == "POST":
        new_rating = request.form['change_rating']
        for i in books:
            i.rating = new_rating
            db.session.commit()
            return redirect(url_for('home'))
    
    return render_template('change.html', n = name, r = rating)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        new_book = Books(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')
@app.route('/delete<i>')
def delete(i):
    for_delete = db.session.query(Books).get(i)
    db.session.delete(for_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

