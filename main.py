from flask import Flask, request, redirect, render_template
import pymysql
import random
import string

app = Flask(__name__)
conn = pymysql.connect(host='localhost', user='shortener_user', password='your_password', database='URL Shortener')
cursor = conn.cursor()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_code = generate_short_code()
    cursor.execute("INSERT INTO urls (short_code, long_url) VALUES (%s, %s)", (short_code, long_url))
    conn.commit()
    return f"Shortened URL: http://127.0.0.1:5000/{short_code}"  # Updated to ensure proper localhost redirection

@app.route('/<short_code>')
def redirect_url(short_code):
    cursor.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
    result = cursor.fetchone()
    if result:
        return redirect(result[0])  # Redirects to the original URL
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
