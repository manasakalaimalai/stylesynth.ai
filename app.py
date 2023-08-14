from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    option5 = request.form['option5']
    # Retrieve other options similarly

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
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
