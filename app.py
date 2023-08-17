from flask import Flask, render_template, request, redirect, url_for
from serpapi import GoogleSearch
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('outfit.html')

@app.route('/submit', methods=['POST'])
def submit():
    option1 = request.form["option1"]
    option2 = request.form["option2"]
    option3 = request.form["option3"]
    option4 = request.form["option4"]
    option5 = request.form["option5"]

    options = [option1, option2, option3, option4, option5]

    query = " ".join(opt for opt in options if opt != "Any")

    print(query)

    params = {
    "api_key": "1260231f7bba0c7bfc657de963706e2d1deaade93938c3cd588f22ab7d195ab8",
    "engine": "google_images",
    "safe": "active",
    "q": query,  # Use the filtered query here
    "google_domain": "google.co.in",
    "gl": "in",
    "hl": "en",
    "location": "Bengaluru, Karnataka, India"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    image_results = results["images_results"][:10]


    # Process the selected options as needed

    db = sqlite3.connect('search_history.db')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?", ('history',))
    result = cursor.fetchone()
    if(result is None):
        cursor.execute('''CREATE TABLE history(gender varchar(20), garment varchar(20), brand varchar(20), fabric varchar(20), color varchar(20))''')
    cursor.execute("INSERT into history(gender, garment, brand, fabric, color) VALUES (?, ?, ?, ?, ?)", (option1, option2, option3, option4, option5))
    db.commit()
    db.close()
    return render_template('home.html', search_results=image_results)


@app.route('/order', methods=['POST'])
def order_product():
    title = request.form.get('title')
    link = request.form.get('link')
    thumbnail = request.form.get('thumbnail')

    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Create the 'products' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            thumbnail TEXT NOT NULL
        )
    ''')

    cursor.execute('INSERT INTO products (title, link, thumbnail) VALUES (?, ?, ?)',
                   (title, link, thumbnail))
    conn.commit()

    return redirect('/orderedthumbsup')

@app.route('/orderedthumbsup')
def ordered_thumbs_up():
    return render_template('orderedthumbsup.html')


@app.route('/orders')
def orders():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, title, link, thumbnail FROM products')
    orders_data = cursor.fetchall()
    
    conn.close()
    
    return render_template('orders.html', orders=orders_data)

if __name__ == "__main__":
    app.run(debug=True)