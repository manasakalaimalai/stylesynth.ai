from flask import Flask, render_template, request, redirect, url_for
from serpapi import GoogleSearch
import sqlite3
from gpt4all import GPT4All
import json
import nltk
from nltk.corpus import stopwords
import replicate

nltk.download('stopwords') 

stop_words = set(stopwords.words('english')) 


def remove_stop_words(sentence): 
    words = sentence.split() 
  
    filtered_words = [word for word in words if word not in stop_words] 
    return ' '.join(filtered_words)

app = Flask(__name__)

model = GPT4All("llama-2-7b-chat.ggmlv3.q4_0.bin")

def generate_response(prompt):
    # Your LLM code here
    response = model.generate(prompt, max_tokens=150)  # Replace with actual model generation code
    return response

@app.route('/', methods=['GET', 'POST'])
def chat():
    response = []
    generated_response = None
    user_input = None
    stable_output = None

    if request.method == 'POST':
        user_input = request.form['user_input']
        response.append(("User:", user_input))
        generated_response = generate_response("Reply like you're a fashion assistant, I need a concise and straightforward answer, only listing the names of the clothes required. " + user_input)
        stable_prompt = remove_stop_words(generated_response)
        generated_response += "\n" + "Here's an option:\n" 
        stable_output = replicate.run("stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",input={"prompt": stable_prompt})
        stable_output=stable_output[0]
        print(stable_output)

    return render_template('outfit.html', response=response, generated_response=generated_response, user_input=user_input, stable_output=stable_output)

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
