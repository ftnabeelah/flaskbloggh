import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

app = Flask(__name__)

# Configure SQLite database using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'

# Initialize the database
db = SQLAlchemy(app)

# Define a model for blog posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Create the tables before processing any requests
@app.before_request
def create_tables():
    db.create_all()

# Homepage route
@app.route('/')
def index():
    posts = Post.query.all()  # Fetch all posts from the SQLite database
    return render_template('index.html', posts=posts)

# Single post route
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)  # Get post by ID or return 404 if not found
    return render_template('post.html', post=post)

# Create post route
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()  # Save the new post to the SQLite database
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)



