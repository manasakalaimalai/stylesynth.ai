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

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response = []
    generated_response = None
    user_input = None
    stable_output = None
    image_results = None

    if request.method == 'POST':
        user_input = request.form['user_input']
        response.append(("User:", user_input))
        generated_response = generate_response("Reply like you're a fashion assistant, I need a concise and straightforward answer, only listing the names of the clothes required. " + user_input)
        stable_prompt = remove_stop_words(generated_response)

        params = {
        "api_key": "1260231f7bba0c7bfc657de963706e2d1deaade93938c3cd588f22ab7d195ab8",
        "engine": "google_images",
        "safe": "active",
        "q": generated_response,  # Use the filtered query here
        "google_domain": "google.co.in",
        "gl": "in",
        "hl": "en",
        "location": "Bengaluru, Karnataka, India"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        image_results = results["images_results"][:2]
        generated_response += "\n" + "Here's an option:\n" 
        stable_output = replicate.run("stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",input={"prompt": stable_prompt})
        stable_output=stable_output[0]

        print(stable_output)

    return render_template('chatbox.html', response=response, generated_response=generated_response, user_input=user_input, stable_output=stable_output, search_results = image_results)

@app.route('/hola', methods=['GET', 'POST'])
def hola():
    return render_template('home.html')

@app.route('/chatbox', methods=['GET', 'POST'])
def chatbox():

    if request.method == 'POST':
        answers_json = request.form.get('answers[]')
        answers = json.loads(answers_json)
        suggested_response = None
        first_stable_output = None

        for idx, answer in enumerate(answers):
            print(f"Answer {idx + 1}: {answer}")

        db = sqlite3.connect('search_history.db')
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?", ('history',))
        cursor.execute("SELECT GARMENT FROM HISTORY GROUP BY GARMENT ORDER BY COUNT(*) DESC LIMIT 1")
        gar = cursor.fetchone()[0]
        cursor.execute("SELECT BRAND FROM HISTORY GROUP BY BRAND ORDER BY COUNT(*) DESC LIMIT 1")
        brnd = cursor.fetchone()[0]
        cursor.execute("SELECT FABRIC FROM HISTORY GROUP BY FABRIC ORDER BY COUNT(*) DESC LIMIT 1")
        fab = cursor.fetchone()[0]
        cursor.execute("SELECT COLOR FROM HISTORY GROUP BY COLOR ORDER BY COUNT(*) DESC LIMIT 1")
        col = cursor.fetchone()[0]
        gar = gar.replace("Any", "")
        brnd = brnd.replace("Any", "")
        fab = fab.replace("Any", "")
        col = col.replace("Any", "")

        print(gar, brnd, fab, col)
        prompt = "A " + col + " " + fab +" " + brnd + " " + gar + " for a " + answers[1] + " year old, " + "living in " + answers[3]+ " with a " + answers[0] + " body type " + " on the occasion of " + answers[2]
        print(prompt)
        first_stable_output = replicate.run("stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",input={"prompt": prompt})
        first_stable_output=first_stable_output[0]

        print(first_stable_output)
        return render_template('chatbox.html', first_stable_output= first_stable_output)
    else:
        return render_template('outfit.html')


@app.route('/', methods=['GET', 'POST'])
def submit():
    image_results = []
    if request.method == 'POST':
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
