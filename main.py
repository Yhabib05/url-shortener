import hashlib
import os
from random import choice
import string
from flask import Flask, request,render_template_string, session, flash, redirect, url_for
from flasgger import Swagger
from library.database import DataBase
from library import app, db

# We limit the hash size to 8
HASH_SIZE = 8
base= "http://127.0.0.1:5000/"
# Input Your customized base Here:
#base = "https://smallurl/"

# We start with a simple db as a Hashmap/dictionary
#db = {}

@app.route("/about")
def about():
    return "<p>The about page</p>"


@app.route("/generate_salt")

# Generates a random salt
def generate_salt():
    return os.urandom(16).hex()

#generate a unique user id
def generate_user_id(num_of_chars: int):
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
            <input type="submit" name="action" value="Shorten URL">
        </form>
        {% if short_url %}
            <p>Shortened URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
        {% endif %}

        <h2>URL Retrieval</h2>
        <form method="POST">
        <label for="url">Enter URL to shorten:</label><br><br>
            <input type="text" id="url" name="short_url_1" required><br><br>
            <input type="submit" name="action" value="Retrieve URL">
        </form>
        {% if long_url_1 %}
            <p>Shortened URL: <a href="{{ long_url_1 }}">{{ long_url_1 }}</a></p>
        {% endif %}  

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul>
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    </body>
</html>
"""



@app.route("/",methods=["GET","POST"])
def index():
    short_url = None
    long_url_1 = None

    if request.method=="POST":
        action = request.form.get('action')

        if action  =="Shorten URL":
            long_url = request.form.get('long_url')  # Retrieve the long URL from the form       
            if not long_url:
                flash('The URL is required!')
            else:
                user_id= generate_user_id(8)
                short_url= shorten_url(user_id, long_url)

        elif action == "Retrieve URL":
            short_url_1=request.form.get('short_url_1') 
            if not short_url_1:
                flash("The short URL is required!")
            else:
                long_url_1 = get_originalUrl(short_url_1)
                
    return render_template_string(form_template, short_url=short_url, long_url_1=long_url_1)


def shorten_url(user_id, long_url):
    hash_ = hashing_function(user_id, long_url)  # Get the hash
    #Old db( dictionary)
    #if short_url not in db:
    #    db[short_url] = {"long_url": long_url, "user_id": user_id}  # Store the mapping as a dictionary
    
    existing_url = DataBase.query.filter_by(hash_url=hash_).first()
    if existing_url:
        return base + existing_url.hash_url

    short_url = base + hash_  # Create the short URL

    # store the new URL in the database
    new_entry = DataBase(long_url=long_url, hash_url=hash_, user_id=user_id)
    db.session.add(new_entry)
    db.session.commit()

    return short_url

# A test function to return the original URL
def get_originalUrl(short_url):
    hash_=short_url.split(base)[1]
    entry = DataBase.query.filter_by(hash_url=hash_).first()
    if entry:
        return entry.long_url
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route("/<hash_url>")
def redirectUrl(hash_url):
    #hash_=short_url.split(base)[1]
    entry = DataBase.query.filter_by(hash_url=hash_url).first()
    if entry:
        return redirect(entry.long_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

        

"""
#Testing function
def main():
    session['user_id'] = generate_user_id(8)
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

