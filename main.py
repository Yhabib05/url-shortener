import hashlib
import os
from random import choice
import string
from flask import Flask, request,render_template_string, session, flash, redirect, url_for
from flasgger import Swagger
from core.database import DataBase

#from sqlalchemy.sql import func
from flask_migrate import Migrate
from core import app, db
#from database import DataBase,db



#db.init_app(app)
#migrate = Migrate(app, db)


# We limit the hash size to 8
HASH_SIZE = 8
base = "https://smallurl/"

# We start with a simple db as a Hashmap/dictionary
#db = {}

@app.route("/about")
def about():
    return "<p>The about page</p>"


@app.route("/generate_salt")
# Generates a random salt
def generate_salt():
    return os.urandom(16).hex()

#generate id
def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    if 'user_id' not in session:
        session['user_id'] = ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))
    return session['user_id']

# Generate a unique shortened URL for each combination of user ID and original URL.
def hashing_function(user_id, long_url):
    url_ = long_url.split('//')[1]  # Remove the protocol
    to_hash = url_ + user_id  
    return hashlib.sha256(to_hash.encode()).hexdigest()[:HASH_SIZE]  # Generate hash



# HTML template for input form
form_template = """
<!DOCTYPE html>
<html>
    <body>
        <h2>URL Shortener</h2>
        <form method="POST">
            <label for="url">Enter URL to shorten:</label><br><br>
            <input type="text" id="url" name="long_url" required><br><br>
            <input type="submit" value="Submit">
        </form>
        {% if short_url %}
            <p>Shortened URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
        {% endif %}
    </body>
</html>
"""



@app.route("/",methods=["GET","POST"])
def index():
    short_url = None
    if request.method=="POST":
        long_url = request.form.get('long_url')  # Retrieve the URL from the form       
        if not long_url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        
        
        user_id= generate_short_id(8)
        short_url= shorten_url(user_id, long_url) 
    return render_template_string(form_template, short_url=short_url)


def shorten_url(user_id, long_url):
    hash_ = hashing_function(user_id, long_url)  # Get the hash
    #Old db( dictionary)
    #if short_url not in db:
    #    db[short_url] = {"long_url": long_url, "user_id": user_id}  # Store the mapping as a dictionary
    
    existing_url = DataBase.query.filter_by(short_id=hash_).first()
    if existing_url:
        return base + existing_url.short_id

    short_url = base + hash_  # Create the short URL

    # Otherwise, store the new URL in the database
    new_entry = DataBase(long_url=long_url, short_id=hash_, user_id=user_id)
    db.session.add(new_entry)
    db.session.commit()

    return short_url

def get_originalUrl(short_url):
    entry = db.get(short_url)  # Look up the original URL in the db
    if entry:
        return entry["long_url"] #, entry["user_id"]  # Return both the original URL and user ID
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

"""
def main():
    session['user_id'] = generate_short_id(8)
    long_url = "https://github.com/Yhabib05/url-shortener.git"
    
    # Shorten the URL
    short_url = shorten_url(session['user_id'], long_url)
    print("Shortened URL:", short_url)
    
    # Retrieve the original URL and user ID
    original_url, retrieved_user_id = get_originalUrl(short_url)
    print("Original URL:", original_url)
    print("User ID:", retrieved_user_id)
"""

if __name__ == "__main__":
    app.run(debug=True)

